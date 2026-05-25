---
title: Spring AI Alibaba快速入门与项目搭建
date: 2026-05-25
tags: AI, Spring AI, Spring AI Alibaba, DashScope, 通义千问
summary: 从零搭建 Spring AI Alibaba 项目，接入通义千问大模型，跑通第一个聊天接口，记录真实踩坑过程。
author: ai-helper
---

## 问题场景

团队决定在内部客服系统中引入大模型能力，需求很明确：用户输入问题，系统调用大模型返回回答。技术选型阶段，我们评估了几种方案：直接调 HTTP API、用 LangChain4j、用 Spring AI。

最终选了 Spring AI Alibaba，原因很简单：团队技术栈是 Spring Boot，Spring AI 是 Spring 官方出品的 AI 抽象层，而 Spring AI Alibaba 是阿里云对这套抽象层的实现，直接对接 DashScope API，能用通义千问系列模型。对我们来说，既不用改技术栈，又不用自己封装 HTTP 调用，省心。

但实际搭起来之后发现，从"看起来简单"到"真正跑通"中间还是有不少坑的。这篇文章就记录整个搭建过程。

## 分析思路

Spring AI 的架构分两层：

1. **Spring AI Core**：定义了统一的抽象接口（ChatClient、EmbeddingModel、VectorStore 等），跟具体模型无关。
2. **Spring AI Alibaba**：基于 Spring AI Core，对接阿里云 DashScope API，支持通义千问、百炼等模型。

我们需要做三件事：
- 引入正确的依赖（版本兼容是第一个坑）
- 配置 DashScope API Key
- 写一个 ChatController 实现基本对话

## 具体实现

### 第一步：Maven 依赖配置

```xml
<!-- pom.xml -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.0</version>
</parent>

<properties>
    <spring-ai.version>1.0.0</spring-ai.version>
    <spring-ai-alibaba.version>1.0.0</spring-ai-alibaba.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Spring AI Alibaba 核心依赖 -->
    <dependency>
        <groupId>com.alibaba.cloud.ai</groupId>
        <artifactId>spring-ai-alibaba-starter</artifactId>
        <version>${spring-ai-alibaba.version}</version>
    </dependency>
</dependencies>

<!-- Spring AI 的仓库，正式版发布后可去掉 -->
<repositories>
    <repository>
        <id>spring-milestones</id>
        <name>Spring Milestones</name>
        <url>https://repo.spring.io/milestone</url>
    </repository>
</repositories>
```

**踩坑提醒**：Spring AI 和 Spring AI Alibaba 的版本必须对齐。我们一开始用的是 Spring AI 1.0.0-M4 + Spring AI Alibaba 1.0.0-M6，结果启动直接报 `NoSuchMethodError`。原因是 Spring AI Alibaba 的某个版本依赖了 Spring AI 的新 API，但引入的是旧版 Core。后来统一用 Release 版本才解决。

### 第二步：配置文件

```yaml
# application.yml
spring:
  ai:
    dashscope:
      api-key: ${DASHSCOPE_API_KEY}
      chat:
        options:
          model: qwen-plus
          temperature: 0.7
          max-tokens: 2000
```

**注意事项**：
- API Key 建议用环境变量，不要硬编码到配置文件里
- `qwen-plus` 是性价比最高的选择，日常开发调试够用；生产环境如果对响应速度要求高，可以用 `qwen-turbo`；如果对质量要求极高，用 `qwen-max`
- `temperature` 越低回答越确定，客服场景建议 0.3-0.5

### 第三步：基础聊天接口

```java
@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
@Slf4j
public class ChatController {

    private final ChatClient chatClient;

    /**
     * 简单对话接口
     * 用户发送消息，返回模型的回答
     */
    @PostMapping("/send")
    public ChatResponse send(@RequestBody ChatRequest request) {
        log.info("【聊天请求】用户输入: {}", request.message());
        ChatResponse response = chatClient.prompt()
                .user(request.message())
                .call()
                .chatResponse();
        log.info("【聊天完成】Token使用: prompt={}, completion={}",
                response.getMetadata().getUsage().getPromptTokens(),
                response.getMetadata().getUsage().getCompletionTokens());
        return response;
    }

    public record ChatRequest(String message) {}
}
```

### 第四步：ChatClient 配置

```java
@Configuration
public class AiConfig {

    @Bean
    public ChatClient chatClient(ChatModel chatModel) {
        return ChatClient.builder(chatModel)
                .defaultSystem("你是一个专业的客服助手，请用简洁友好的语言回答用户的问题。")
                .build();
    }
}
```

这里有个容易忽略的点：`ChatModel` 是 Spring AI 自动装配的 Bean，Spring AI Alibaba 的 starter 会根据配置自动创建 `DashScopeChatModel`。不需要手动 `new`。

### 验证

启动应用，用 curl 测试：

```bash
curl -X POST http://localhost:8080/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，请问你们的工作时间是什么？"}'
```

正常情况下会返回一个 JSON 响应，包含模型的回答内容。

## 进阶：自定义自动装配

如果项目中有多个 DashScope 实例（比如测试环境和生产环境用不同的 Key），可以自定义配置：

```java
@Configuration
public class MultiDashScopeConfig {

    @Bean("prodChatModel")
    public ChatModel prodChatModel() {
        DashScopeApi api = DashScopeApi.builder()
                .apiKey(System.getenv("PROD_DASHSCOPE_KEY"))
                .build();
        return new DashScopeChatModel(api,
                DashScopeChatOptions.builder()
                        .withModel("qwen-max")
                        .withTemperature(0.3)
                        .build());
    }

    @Bean("testChatModel")
    public ChatModel testChatModel() {
        DashScopeApi api = DashScopeApi.builder()
                .apiKey(System.getenv("TEST_DASHSCOPE_KEY"))
                .build();
        return new DashScopeChatModel(api,
                DashScopeChatOptions.builder()
                        .withModel("qwen-plus")
                        .withTemperature(0.7)
                        .build());
    }
}
```

## 踩坑总结

1. **版本兼容是最大坑**：Spring AI 还在快速迭代，Spring AI Alibaba 的版本也要跟着走。建议锁定版本后写个集成测试，确保基本调用链路没问题再往上加功能。

2. **依赖冲突**：Spring AI 依赖了一些跟 Spring Boot 主版本相关的库。如果项目里有 `spring-boot-starter-webflux` 或者其他版本较老的依赖，容易出现 jar 包冲突。用 `mvn dependency:tree` 排查。

3. **自动装配不生效**：如果 `ChatModel` 注入失败，检查启动类有没有 `@ComponentScan` 覆盖了自动装配的包路径。Spring AI 的自动配置类在 `org.springframework.ai.autoconfigure` 包下，别把它排除了。

4. **API Key 安全**：开发环境可以用 `.env` 文件配合 `spring.config.import=optional:file:.env`，生产环境必须用配置中心或环境变量。

5. **本地调试效率**：DashScope 的调用有网络延迟，每次改动重启太慢。建议写单元测试时 Mock `ChatModel`，只在集成测试时真正调 API。

整体来看，Spring AI Alibaba 的接入门槛不高，核心就是搞定依赖版本 + 配置 API Key + 写 Controller。真正的挑战在后续的功能拓展上，比如 RAG、Function Calling、多模型切换，这些会在后续文章中详细展开。
