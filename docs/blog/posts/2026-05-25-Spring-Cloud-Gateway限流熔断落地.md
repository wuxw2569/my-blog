---
title: Spring Cloud Gateway限流熔断落地
date: 2020-07-16
tags: 架构, Spring Cloud Gateway, Sentinel, 限流, 熔断
summary: Gateway结合Sentinel/Resilience4j在中小厂的落地实战，含配置细节与限流策略选型
author: ai-helper
---

## 背景：为什么我们扛不住一次促销

我们是一个日活 20 万的电商后台，团队 60 人。去年双十一大促，一个商品详情接口 QPS 从平时的 500 飙到 5000，后端直接雪崩。复盘之后，决定在网关层做限流和熔断。

技术栈：Spring Cloud Gateway 4.1.x + Spring Boot 3.2 + Nacos 2.3

## Sentinel vs Resilience4j：选型考量

| 维度 | Sentinel | Resilience4j |
|------|----------|-------------|
| 生态 | 阿里系，和 Nacos/SCA 配套好 | Netflix 系，Spring Cloud 原生支持 |
| 控制台 | 自带 Dashboard，实时监控 | 无自带控制台，需配合 Prometheus |
| 学习成本 | 概念多（流控规则、降级规则、热点规则） | 概念清晰（CircuitBreaker、RateLimiter、Bulkhead） |
| 限流精度 | 滑动窗口/令牌桶/漏桶都有 | 只有令牌桶 |
| 适合场景 | 需要动态规则推送、有控制台需求 | 偏好轻量、和 Micrometer 集成 |

我们选了 **Sentinel**，原因很简单：团队已经在用 Nacos，Sentinel + Nacos 做动态规则推送几乎零成本，而且 Dashboard 免费用，省得自己搭监控。

## 网关层限流配置

### 依赖引入

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    <version>2023.0.1.0</version>
</dependency>
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-alibaba-sentinel-gateway</artifactId>
    <version>2023.0.1.0</version>
</dependency>
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-datasource-nacos</artifactId>
    <version>1.8.8</version>
</dependency>
```

### Nacos 动态规则配置

```yaml
spring:
  cloud:
    sentinel:
      datasource:
        gw-flow:
          nacos:
            server-addr: ${NACOS_ADDR:127.0.0.1:8848}
            data-id: gateway-flow-rules
            group-id: SENTINEL_GROUP
            data-type: json
            rule-type: gw-flow
```

Nacos 中 `gateway-flow-rules` 的内容：

```json
[
  {
    "resource": "product-detail",
    "limitApp": "default",
    "grade": 1,
    "count": 1000,
    "strategy": 0,
    "controlBehavior": 0,
    "burst": 200
  },
  {
    "resource": "order-create",
    "limitApp": "default",
    "grade": 1,
    "count": 500,
    "strategy": 0,
    "controlBehavior": 2,
    "maxQueueingTimeMs": 500
  }
]
```

关键参数说明：
- `grade=1` 表示 QPS 限流（0 是线程数限流）
- `count` 是阈值
- `controlBehavior=0` 是直接拒绝，`2` 是排队等待
- `burst` 是突发流量容忍值，应对瞬时峰值

### 网关路由配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: product-service
          uri: lb://product-service
          predicates:
            - Path=/api/product/**
          metadata:
            # 这个 resource 名要和 Nacos 规则里的 resource 对应
            sentinel.resource.name: product-detail
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/order/**
          metadata:
            sentinel.resource.name: order-create
```

## 限流策略选择

我们针对不同接口用了不同策略：

**商品详情（读多写少）**：QPS 限流 + 预热模式

```java
// 代码方式配置预热，也可以在 Nacos 规则里配
@GetMapping("/api/product/{id}")
@SentinelResource(value = "product-detail",
    blockHandler = "handleBlock",
    fallback = "handleFallback")
public Result<ProductVO> detail(@PathVariable Long id) {
    return productService.getDetail(id);
}
```

Sentinel 的 warm up 模式会在系统刚启动时，逐步提升限流阈值，避免冷启动时被打满。配置方式是 `controlBehavior=3` + `warmUpPeriodSec=10`（10 秒预热期）。

**下单接口（写操作）**：排队等待 + 熔断降级

```yaml
# Sentinel 降级规则 - 慢调用比例熔断
[
  {
    "resource": "order-create",
    "grade": 0,
    "count": 500,
    "slowRatioThreshold": 0.5,
    "timeWindow": 30,
    "minRequestAmount": 10,
    "statIntervalMs": 10000
  }
]
```

意思是：10 秒内至少 10 个请求，如果慢调用（超过 500ms）比例超过 50%，就熔断 30 秒。

## 全局兜底返回

限流被拒后需要返回友好的 JSON，而不是 Sentinel 默认的 `Blocked by Sentinel` 文本：

```java
@Component
public class SentinelGatewayConfig {

    @PostConstruct
    public void init() {
        GatewayCallbackManager.setBlockHandler(
            (exchange, e) -> {
                ServerHttpResponse response = exchange.getResponse();
                response.setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
                response.getHeaders().setContentType(MediaType.APPLICATION_JSON);

                String body = "{\"code\":429001,\"message\":\"请求过于频繁，请稍后重试\"}";
                DataBuffer buffer = response.bufferFactory().wrap(body.getBytes());
                return response.writeWith(Mono.just(buffer));
            }
        );
    }
}
```

## 生产环境踩坑

1. **Sentinel 和 Gateway 整合的版本问题**：Sentinel 1.8.x 对 Spring Cloud Gateway 4.x 的支持有坑，需要至少 1.8.7+。我们一开始用了 1.8.4，网关直接启动报错 `NoSuchMethodError`。

2. **规则推送不生效**：Nacos 的 `data-type` 必须是 `json`，`rule-type` 必须是 `gw-flow`（不是 `flow`），否则规则推送了但 Sentinel 不认。这个坑我们排查了大半天。

3. **集群限流的坑**：Sentinel 的集群限流需要独立的 Token Server，中小厂不建议上。我们试过，Token Server 自己成了单点，维护成本太高。单机限流 + Nginx 层的 `limit_req` 就够了。

4. **熔断恢复时间**：`timeWindow` 别设太长。我们设了 60 秒，结果服务恢复了但流量进不来，白白损失了 30 秒的请求。建议 15-30 秒，配合健康检查一起看。

5. **监控告警**：Sentinel Dashboard 的数据只保留 5 分钟，生产环境一定要把 Sentinel 的 Metric 指标推到 Prometheus，配合 Grafana 做告警。我们用的是 `sentinel-transport-simple-http` 暴露 `/metric` 端点。

## 最终效果

上线后压测结果：

- 商品详情接口从无限流时的 3000 QPS（后面直接超时），变成稳定的 1000 QPS + 200 突发，P99 延迟控制在 200ms 以内
- 下单接口在慢调用比例超标时自动熔断，30 秒后自动恢复，不再雪崩
- 前端在限流时收到 `429` 状态码和友好提示，而不是白屏

整体投入 2 人周，性价比很高。对中小厂来说，网关层限流是性价比最高的稳定性投资。
