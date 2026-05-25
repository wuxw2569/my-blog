---
title: Spring AI Function Calling工具调用实战
date: 2026-05-25
tags: AI, Spring AI, Function Calling, 工具调用, DashScope
summary: 用 Spring AI 实现 Function Calling，让大模型调用真实业务接口，查订单、查库存、发通知，完整实战经验。
author: ai-helper
---

## 问题场景

大模型能回答通用问题，但涉及到业务数据就无能为力了。比如用户问"我上周下的订单到哪了"，模型不可能知道。这时候需要让模型有能力"调用"我们的业务接口。

这就是 Function Calling（函数调用）：模型根据用户意图，决定要调用哪个函数、传什么参数，然后把函数的返回结果融入回答中。

听起来很美好，但实际接入过程中，函数定义格式、参数绑定、多工具编排、异常处理都有坑。

## 分析思路

Spring AI 对 Function Calling 的支持流程是：

1. 定义 Java 方法（就是普通的 Service 方法）
2. 用 `@Description` 注解描述函数用途和参数说明
3. 注册到 ChatClient
4. 模型在对话中决定是否调用

关键在于：模型能不能正确理解你的函数描述，以及能不能生成正确的参数。这取决于你的描述写得够不够清楚。

## 具体实现

### 第一步：定义工具函数

```java
/**
 * 订单查询工具
 * 函数描述写得越清晰，模型调用越准确
 */
@Service
@Slf4j
public class OrderQueryTool {

    private final OrderService orderService;

    public OrderQueryTool(OrderService orderService) {
        this.orderService = orderService;
    }

    /**
     * 根据订单号查询订单详情
     * 模型会从用户消息中提取订单号来调用这个函数
     */
    @Description("根据订单编号查询订单详情，包括订单状态、物流信息、商品信息。订单编号格式一般为 ORD 开头的字符串。")
    public OrderResult queryOrder(
            @Description("订单编号，例如 ORD20240101001") String orderNo) {
        log.info("【工具调用】查询订单: {}", orderNo);
        try {
            Order order = orderService.findByOrderNo(orderNo);
            if (order == null) {
                return new OrderResult(false, "未找到订单 " + orderNo, null);
            }
            return new OrderResult(true, "查询成功", order);
        } catch (Exception e) {
            log.error("【工具调用异常】查询订单失败: {}", e.getMessage());
            return new OrderResult(false, "查询出错: " + e.getMessage(), null);
        }
    }

    /**
     * 查询用户的最近订单列表
     */
    @Description("查询指定用户最近的订单列表，返回最近N条订单的基本信息。当用户问'我的订单'、'最近买了什么'时使用此函数。")
    public List<OrderBrief> queryRecentOrders(
            @Description("用户ID") Long userId,
            @Description("查询数量，默认5条") Integer limit) {
        log.info("【工具调用】查询用户最近订单: userId={}, limit={}", userId, limit);
        if (limit == null || limit <= 0) {
            limit = 5;
        }
        return orderService.findRecentOrders(userId, Math.min(limit, 20));
    }

    public record OrderResult(boolean success, String message, Order order) {}

    public record OrderBrief(String orderNo, String status, BigDecimal amount, String createTime) {}
}
```

```java
/**
 * 库存查询工具
 */
@Service
@Slf4j
public class InventoryTool {

    private final InventoryService inventoryService;

    public InventoryTool(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @Description("查询商品的库存数量。用户问'还有货吗'、'库存多少'时使用此函数。")
    public InventoryResult checkStock(
            @Description("商品名称或SKU编号") String product,
            @Description("仓库编号，不传则查询所有仓库汇总") String warehouse) {
        log.info("【工具调用】查询库存: product={}, warehouse={}", product, warehouse);
        try {
            int stock = inventoryService.getStock(product, warehouse);
            boolean available = stock > 0;
            return new InventoryResult(product, stock, available,
                    available ? "有货" : "暂时缺货");
        } catch (Exception e) {
            return new InventoryResult(product, -1, false, "查询失败: " + e.getMessage());
        }
    }

    public record InventoryResult(String product, int stock, boolean available, String message) {}
}
```

### 第二步：注册工具到 ChatClient

```java
@Configuration
public class ToolConfig {

    @Bean
    public ChatClient chatClient(ChatModel chatModel,
                                  OrderQueryTool orderTool,
                                  InventoryTool inventoryTool) {
        return ChatClient.builder(chatModel)
                .defaultSystem("""
                        你是一个智能客服助手。你可以帮用户查询订单和库存信息。
                        使用工具时，请确保参数准确。如果用户信息不完整，先向用户确认再调用工具。
                        """)
                // 注册工具函数
                .defaultFunctions("queryOrder", "queryRecentOrders", "checkStock")
                .build();
    }
}
```

### 第三步：对话接口

```java
@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
@Slf4j
public class ToolChatController {

    private final ChatClient chatClient;

    @PostMapping("/tool")
    public Map<String, Object> chatWithTools(@RequestBody ChatRequest request) {
        log.info("【工具对话】用户输入: {}", request.message());

        // Spring AI 会自动处理 Function Calling 的完整流程：
        // 1. 把用户消息 + 可用函数列表发给模型
        // 2. 模型返回要调用的函数及参数
        // 3. Spring AI 自动调用函数获取结果
        // 4. 把函数返回结果再发给模型生成最终回答
        String answer = chatClient.prompt()
                .user(request.message())
                .call()
                .content();

        return Map.of("answer", answer);
    }

    public record ChatRequest(String message) {}
}
```

### 第四步：多工具编排（复杂场景）

有些场景需要模型连续调用多个工具。比如用户问"我订单里的商品还有货吗？换货的话库存够吗"，需要先查订单 -> 再查库存。

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class OrderInventoryTool {

    private final OrderService orderService;
    private final InventoryService inventoryService;

    /**
     * 复合工具：查订单 + 查关联商品库存
     * 避免模型分两次调用，减少延迟
     */
    @Description("查询订单及其商品的库存情况。当用户想了解订单中商品是否有货、能否换货时使用。")
    public OrderStockResult checkOrderStock(
            @Description("订单编号") String orderNo) {
        log.info("【复合工具】查询订单库存: {}", orderNo);

        Order order = orderService.findByOrderNo(orderNo);
        if (order == null) {
            return new OrderStockResult(false, "订单不存在", List.of());
        }

        List<ProductStock> stocks = order.getItems().stream()
                .map(item -> {
                    int stock = inventoryService.getStock(item.getSku(), null);
                    return new ProductStock(item.getProductName(), item.getSku(), stock);
                })
                .toList();

        return new OrderStockResult(true, "查询成功", stocks);
    }

    public record OrderStockResult(boolean success, String message, List<ProductStock> stocks) {}
    public record ProductStock(String productName, String sku, int stock) {}
}
```

### 自定义 FunctionCallback（高级用法）

如果注解方式不够灵活，可以手动注册：

```java
@Configuration
public class ManualToolConfig {

    @Bean
    public FunctionCallbackResolver functionCallbackResolver() {
        FunctionCallbackResolver resolver = new FunctionCallbackResolver();

        // 手动注册一个动态函数
        resolver.registerFunction("sendNotification",
                new FunctionCallback() {
                    @Override
                    public String getName() {
                        return "sendNotification";
                    }

                    @Override
                    public String getDescription() {
                        return "发送通知给用户，支持短信和邮件";
                    }

                    @Override
                    public String call(String args) {
                        // args 是 JSON 格式的参数
                        JsonNode params = JsonUtil.parse(args);
                        String userId = params.get("userId").asText();
                        String message = params.get("message").asText();
                        String channel = params.get("channel").asText();
                        // 调用通知服务
                        return sendNotification(userId, message, channel);
                    }
                });

        return resolver;
    }
}
```

## 踩坑总结

1. **`@Description` 注解写不好，模型就乱调**：这是 Function Calling 最大的坑。描述必须精确说明：什么场景下用这个函数、参数是什么格式、有哪些边界条件。我们一开始描述写得太简单，模型经常在不该调的时候调了，或者传了错误格式的参数。

2. **参数校验必须做**：模型生成的参数不一定靠谱，可能是空字符串、格式不对、甚至注入恶意内容。每个工具函数的入参都要做严格校验。

3. **函数数量不宜太多**：注册了 10 个以上的函数后，模型的选择准确率明显下降。建议按场景分组，每次对话只注册相关的函数。

4. **DashScope 的 Function Calling 兼容性**：通义千问对 Function Calling 的支持在不同模型版本间有差异。qwen-turbo 对复杂参数结构（嵌套对象）的支持不太好，建议参数尽量用扁平结构。qwen-plus 和 qwen-max 支持更好。

5. **超时和重试**：工具函数可能涉及数据库查询或外部 API 调用，如果执行慢了，整个对话链路都会变长。建议工具函数内部设超时（比如 5 秒），超时返回一个明确的错误信息让模型知道。

6. **日志必须完整**：每次工具调用都要记录：模型决定调用什么函数、传了什么参数、返回了什么结果。这是排查问题的关键线索。我们生产环境出过一次"模型持续调用错误函数"的问题，就是因为日志不全，排查了很久。
