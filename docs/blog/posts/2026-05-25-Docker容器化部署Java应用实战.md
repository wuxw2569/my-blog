---
title: Docker容器化部署Java应用实战
date: 2026-03-11
tags: Docker, Java, 容器化, 部署, DevOps
summary: 从实际项目出发，分享Dockerfile编写最佳实践、多阶段构建、JVM容器化内存配置与日志管理的踩坑经验。
author: ai-helper
---

### 问题场景

我们团队（80人规模，Java后端为主）在2024年初开始全面容器化迁移。最初的Dockerfile是开发同学随手写的，一个Spring Boot应用镜像竟然打到了1.2GB，启动时间超过60秒，线上还频繁出现OOM。这篇文章记录了我们从"能跑就行"到"生产可用"的完整过程。

### 多阶段构建：镜像从1.2GB瘦身到280MB

第一版Dockerfile很朴素——把本地打好的jar直接COPY进去：

```dockerfile
# 反面教材：直接用JDK基础镜像 + 拷贝fat jar
FROM openjdk:17
COPY target/app.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

问题很明显：openjdk:17 基础镜像约 500MB，加上jar包和各种缓存层，镜像体积巨大。

**改进方案：多阶段构建**

```dockerfile
# ============ 阶段1：构建 ============
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
# 先拷贝pom，利用Docker层缓存加速依赖下载
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn package -DskipTests -B

# ============ 阶段2：运行 ============
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
# 只拷贝构建产物
COPY --from=builder /build/target/app.jar app.jar
# 创建非root用户运行
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**踩坑点**：
- `eclipse-temurin:17-jre-alpine` 比完整JDK镜像小很多，生产环境只需要JRE
- 拷贝 pom.xml 单独执行 `dependency:go-offline` 是利用Docker层缓存的关键——只要 pom.xml 不变，依赖下载这一层就不会重新构建
- 用非root用户运行是安全审计的硬性要求

### JVM 容器化内存配置：别再被OOM搞得半夜起来重启

这是我们踩坑最深的地方。Java应用跑在容器里，JVM默认会根据物理机内存分配堆大小，而不是容器限制。一个被限制了512MB的容器，JVM可能尝试分配4GB堆内存，直接被内核OOM Kill。

**Java 17 + 容器感知**

JDK 10+ 默认开启了 `-XX:+UseContainerSupport`，但光靠这个不够。我们的配置：

```dockerfile
ENTRYPOINT ["java", \
  "-XX:+UseContainerSupport", \
  "-XX:MaxRAMPercentage=70.0", \
  "-XX:InitialRAMPercentage=50.0", \
  "-XX:+HeapDumpOnOutOfMemoryError", \
  "-XX:HeapDumpPath=/app/logs/heapdump.hprof", \
  "-XX:+UseG1GC", \
  "-XX:MaxGCPauseMillis=200", \
  "-Djava.security.egd=file:/dev/./urandom", \
  "-jar", "app.jar"]
```

**关键参数说明**：
- `MaxRAMPercentage=70.0`：堆内存最多占容器内存的70%，剩下30%给Metaspace、线程栈、NIO DirectBuffer等
- `HeapDumpOnOutOfMemoryError`：OOM时自动dump，线上排查必备
- `-Djava.security.egd`：加速随机数生成，否则在容器中/dev/random可能阻塞导致启动慢

**实际配比建议**（来自我们踩过的坑）：

| 容器内存 | 堆内存设置 | 说明 |
|---------|-----------|------|
| 512MB | MaxRAMPercentage=60 | 小服务，留够非堆空间 |
| 1GB | MaxRAMPercentage=70 | 中等服务 |
| 2GB+ | MaxRAMPercentage=75 | 大服务 |

### 日志管理：别让容器日志撑爆磁盘

容器环境下，日志写到stdout/stderr是最推荐的做法。但Spring Boot默认的日志配置会写文件，需要调整：

```yaml
# application.yml
logging:
  file:
    name: ""  # 禁用文件日志
  level:
    root: INFO
    com.ourcompany: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] [%X{traceId}] %-5level %logger{36} - %msg%n"
```

**生产环境还需要配置日志轮转**，在docker-compose或K8s层面：

```yaml
# docker-compose.yml
services:
  app:
    image: ourapp:latest
    logging:
      driver: json-file
      options:
        max-size: "50m"    # 单个日志文件最大50MB
        max-file: "5"      # 最多保留5个文件
```

**曾经的教训**：线上一台机器跑了12个容器，没配日志轮转，3天后磁盘满了导致所有服务不可用。`docker system prune` 只能救急，不是长久方案。

### Docker Compose 编排实战

本地开发和小规模生产环境，docker-compose 就够了：

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - JAVA_OPTS=-Xms512m -Xmx512m
    deploy:
      resources:
        limits:
          memory: 768M    # 硬限制
          cpus: '2.0'
        reservations:
          memory: 512M    # 软限制
          cpus: '1.0'
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 踩坑总结

1. **不要用latest标签**：`FROM openjdk:17` 换成 `FROM eclipse-temurin:17-jre-alpine`，指定精确版本避免基础镜像变动导致构建失败
2. **`.dockerignore` 很重要**：不加的话 `.git`、`node_modules`、target里的旧包都会被COPY进去，拖慢构建
3. **健康检查不能少**：K8s和Docker Swarm都依赖健康检查判断服务是否可用，没有健康检查=没有优雅重启
4. **优雅停机**：Spring Boot需要配置 `server.shutdown=graceful` 和 `spring.lifecycle.timeout-per-shutdown-phase=30s`，否则容器停止时正在处理的请求会直接中断
5. **多阶段构建的缓存**：把变化频率低的层（如依赖下载）放在前面，变化频率高的层（如代码编译）放在后面，能显著加速CI构建

容器化不是简单地把jar塞进镜像就完事了。内存配置、日志管理、健康检查、优雅停机，这些细节决定了你的服务能不能在凌晨三点安安静静地运行。
