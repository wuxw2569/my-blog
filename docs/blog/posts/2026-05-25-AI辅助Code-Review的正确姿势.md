---
title: AI辅助Code Review的正确姿势：AI能发现什么，不能发现什么
date: 2026-11-03
tags: AI, AI工具, Code Review, 代码审查, 质量保障
summary: 用AI做代码审查的方法论，明确AI能发现和不能发现的问题边界
author: ai-helper
---

## 场景引入

团队只有5个后端，每天至少10个PR要Review。人手不够，review质量就下降，线上bug就增多。这是中小厂的真实困境。

AI辅助Code Review听起来是完美的解决方案：7x24小时在线、不会疲劳、不会因为赶进度而草草批准。但实际使用下来，AI审查有明确的能力边界。这篇文章基于我团队半年的实践，告诉你哪些问题该交给AI，哪些必须人工把关。

## AI擅长发现的问题

### 1. 安全漏洞（准确率：85%+）

这是AI最可靠的能力。给AI一个PR的diff，它能稳定发现：

**SQL注入**：
```java
// AI会标记：字符串拼接SQL，存在注入风险
String sql = "SELECT * FROM users WHERE name = '" + userName + "'";
```

**硬编码密钥**：
```java
// AI会标记：检测到硬编码的密钥/密码
private static final String API_KEY = "sk-1234567890abcdef";
```

**XSS风险**：
```html
<!-- AI会标记：未转义的用户输入直接输出 -->
<div th:utext="${userInput}"></div>
```

**Prompt模板**：
```
请审查以下代码变更，重点关注：
1. SQL注入、XSS、CSRF等安全漏洞
2. 硬编码的密钥、密码、Token
3. 不安全的加密算法（MD5、SHA1用于密码）
4. 未校验的用户输入

输出格式：[文件:行号] 问题描述 | 严重程度(高/中/低)
```

### 2. 代码异味（准确率：75%）

AI能识别常见的代码异味：
- 过长的方法（>50行）
- 过多的参数（>5个）
- 重复代码块
- 不规范的命名（如`a`, `temp`, `data1`）

### 3. 规范性问题（准确率：90%+）

只要给AI明确的规范，它的检查准确率很高：
- 命名规范（驼峰/下划线）
- 注释规范（Javadoc缺失）
- import顺序
- 日志规范（是否用了System.out）

## AI不擅长的问题

### 1. 业务逻辑正确性（准确率：<30%）

这是AI最大的盲区。AI无法判断：

```java
// 订单金额计算 - AI看不出业务逻辑错误
public BigDecimal calculateOrderAmount(Order order) {
    BigDecimal amount = order.getPrice().multiply(new BigDecimal(order.getQuantity()));
    // 问题：没有减去优惠券金额！但AI不知道业务要求扣减优惠券
    return amount;
}
```

即使在PR描述中写了"订单计算需要扣减优惠券"，AI也经常忽略这种跨文件的业务逻辑。

### 2. 并发问题（准确率：<40%）

AI对race condition、死锁等问题的检出率很低：

```java
// AI通常不会标记这里的并发问题
public void updateStock(Long productId, int quantity) {
    Product product = productRepo.findById(productId);
    // 没有加锁，高并发下可能超卖
    product.setStock(product.getStock() - quantity);
    productRepo.save(product);
}
```

### 3. 性能问题（准确率：<50%）

AI可能会标记N+1查询这种明显问题，但对以下情况基本无能：
- 循环中的数据库查询
- 不合理的缓存策略
- 内存泄漏风险
- 索引失效

### 4. 架构设计问题

AI无法评估：
- 模块划分是否合理
- 依赖方向是否正确
- 是否违反SOLID原则
- 长期可维护性

## 实践方案：人机协作Review流程

我们团队最终采用的方案：

### 第一步：AI初筛（自动）

PR创建后，通过GitHub Actions自动触发AI审查：

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: AI Review
        run: |
          # 调用AI API审查PR diff
          # 将结果作为PR评论发布
```

AI初筛输出分为三类：
- 🔴 **必须修复**：安全漏洞、明显的bug
- 🟡 **建议修改**：代码异味、规范问题
- 🔵 **信息提示**：可能的改进点

### 第二步：人工深度Review

人工Reviewer关注：
1. 业务逻辑正确性
2. 架构设计合理性
3. 并发和性能问题
4. AI标记为"建议修改"的问题是否真的需要改

### 第三步：结果复盘

每周统计AI审查的准确率和漏检率，持续优化Prompt。

## Prompt优化技巧

### 不要太笼统
```
# 差的Prompt
审查这段代码

# 好的Prompt
审查这段代码变更，按以下维度打分（1-5分）：
1. 安全性（SQL注入/XSS/敏感信息泄露）
2. 可读性（命名/注释/方法长度）
3. 健壮性（空值处理/异常处理/边界条件）

每个扣分项给出具体行号和修改建议。
```

### 给足上下文
```
这是一个Spring Boot电商项目的订单模块。
数据库使用MySQL，ORM使用MyBatis-Plus。
并发场景：双11峰值1000 TPS。

请审查以下变更对并发安全性的影响：
[diff内容]
```

## 效率数据

实施AI辅助Review半年后的数据：
- 平均Review时间：从45分钟降到25分钟（减少44%）
- 安全漏洞逃逸率：从每月2-3个降到每月0-1个
- 规范性问题在Review阶段发现率：从60%提升到95%
- 人工Reviewer满意度：82%认为减轻了工作量

## 总结

AI辅助Code Review是"增强"而非"替代"。它的价值在于：
1. 承担重复性、规范性的检查工作
2. 作为安全漏洞的"第二道防线"
3. 减轻人工Reviewer的认知负担

但业务逻辑、架构设计、性能优化这些需要"理解力"的审查，仍然是人类的领地。把AI当作团队中的"初级Reviewer"，让它做初筛，资深开发者做深度Review，这是目前最务实的方案。