---
title: Spring AOP在业务中的实战技巧
date: 2026-05-25
tags: 架构, Spring AOP, 切面, 日志, 权限, 数据脱敏
summary: AOP在日志切面、权限校验、数据脱敏、操作审计、分布式锁中的实战封装技巧
author: ai-helper
---

## AOP 的价值：把横切关注点从业务代码中剥离

刚开始写 Spring Boot 项目时，我习惯在每个 Controller 方法开头写日志、每个 Service 方法开头做权限校验。代码越写越臃肿，加一个通用逻辑要改几十个方法。

AOP（面向切面编程）就是为了解决这个问题——把日志、权限、脱敏这些"横切关注点"从业务代码中剥离出来，统一管理。

以下是我们团队在实际项目中用得最多的 5 个 AOP 场景。

## 场景一：接口日志切面

记录每个 Controller 方法的入参、出参、耗时，用于排查问题。

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface ApiLog {
    /** 模块名称 */
    String module() default "";
    /** 是否记录请求体（大文件上传等场景要关掉） */
    boolean logArgs() default true;
    /** 是否记录响应体 */
    boolean logResult() default true;
}
```

```java
@Aspect
@Component
@Slf4j
public class ApiLogAspect {

    @Around("@annotation(apiLog)")
    public Object around(ProceedingJoinPoint pjp, ApiLog apiLog) throws Throwable {
        String method = pjp.getSignature().toShortString();
        long start = System.currentTimeMillis();

        // 记录入参
        if (apiLog.logArgs()) {
            Object[] args = pjp.getArgs();
            // 坑：参数里可能有 HttpServletRequest 等不可序列化的对象
            String argsStr = safeSerialize(args);
            log.info("【接口入参】{} | {} | args={}", apiLog.module(), method, argsStr);
        }

        try {
            Object result = pjp.proceed();
            long cost = System.currentTimeMillis() - start;

            // 记录出参
            if (apiLog.logResult()) {
                // 坑：响应体可能很大（列表查询返回几千条记录），截断处理
                String resultStr = safeSerialize(result);
                if (resultStr.length() > 2000) {
                    resultStr = resultStr.substring(0, 2000) + "...(truncated)";
                }
                log.info("【接口出参】{} | {} | cost={}ms | result={}",
                    apiLog.module(), method, cost, resultStr);
            } else {
                log.info("【接口完成】{} | {} | cost={}ms", apiLog.module(), method, cost);
            }

            return result;
        } catch (Throwable e) {
            long cost = System.currentTimeMillis() - start;
            log.error("【接口异常】{} | {} | cost={}ms", apiLog.module(), method, cost, e);
            throw e;
        }
    }

    private String safeSerialize(Object obj) {
        try {
            return JSON.toJSONString(obj);
        } catch (Exception e) {
            return "[序列化失败: " + e.getMessage() + "]";
        }
    }
}
```

使用：

```java
@ApiLog(module = "订单模块")
@GetMapping("/api/order/{id}")
public Result<OrderVO> getOrder(@PathVariable Long id) {
    return Result.ok(orderService.getById(id));
}
```

## 场景二：权限校验切面

用自定义注解替代在每个方法里写 `if (!hasPermission(...))` 的代码。

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequirePermission {
    /** 权限标识 */
    String value();
    /** 权限校验失败时的消息 */
    String message() default "无操作权限";
}
```

```java
@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class PermissionAspect {

    private final AuthService authService;

    @Before("@annotation(requirePermission)")
    public void checkPermission(RequirePermission requirePermission) {
        // 从 SecurityContext 获取当前用户
        Long userId = SecurityContextHolder.getCurrentUserId();
        if (userId == null) {
            throw new BizException(401, "未登录");
        }

        boolean hasPermission = authService.hasPermission(
            userId, requirePermission.value());

        if (!hasPermission) {
            log.warn("【权限校验失败】userId={}, permission={}",
                userId, requirePermission.value());
            throw new BizException(403, requirePermission.message());
        }
    }
}
```

使用：

```java
@RequirePermission("order:delete")
@DeleteMapping("/api/order/{id}")
public Result<Void> deleteOrder(@PathVariable Long id) {
    orderService.delete(id);
    return Result.ok(null);
}
```

**踩坑**：AOP 切面默认只能拦截 Spring 代理对象的方法调用。如果在同一个类内部调用（`this.method()`），AOP 不生效。这是最常见的"切面不起作用"的原因。解决方式：

```java
// 方式一：注入自身代理
@Lazy
@Autowired
private OrderService self;

// 方式二：从 AopContext 获取代理（需要开启 exposeProxy）
((OrderService) AopContext.currentProxy()).internalMethod();
```

## 场景三：数据脱敏

敏感数据（手机号、身份证、银行卡）在接口返回时需要脱敏处理。

```java
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Sensitive {
    SensitiveType value();
}

public enum SensitiveType {
    PHONE,      // 手机号：138****1234
    ID_CARD,    // 身份证：110***********1234
    BANK_CARD,  // 银行卡：6222 **** **** 1234
    EMAIL       // 邮箱：t***@example.com
}
```

```java
@Aspect
@Component
public class SensitiveDataAspect {

    /**
     * 对 Controller 返回值中的敏感字段做脱敏
     * 坑：@AfterReturning 的返回值修改需要特殊处理
     */
    @AfterReturning(pointcut = "execution(* com.example..controller..*(..))",
        returning = "result")
    public void desensitize(Object result) {
        if (result == null) return;
        // 处理 Result 包装类
        if (result instanceof Result<?> wrapper) {
            Object data = wrapper.getData();
            if (data != null) {
                desensitizeObject(data);
            }
        }
    }

    private void desensitizeObject(Object obj) {
        // 反射遍历字段，对带 @Sensitive 注解的字段做脱敏
        for (Field field : obj.getClass().getDeclaredFields()) {
            Sensitive annotation = field.getAnnotation(Sensitive.class);
            if (annotation != null) {
                field.setAccessible(true);
                try {
                    String value = (String) field.get(obj);
                    if (value != null) {
                        field.set(obj, mask(value, annotation.value()));
                    }
                } catch (IllegalAccessException e) {
                    // 忽略
                }
            }
        }
    }

    private String mask(String value, SensitiveType type) {
        return switch (type) {
            case PHONE -> value.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2");
            case ID_CARD -> value.replaceAll("(\\d{3})\\d{11}(\\d{4})", "$1***********$2");
            case BANK_CARD -> value.replaceAll("(\\d{4})\\d{8,12}(\\d{4})", "$1 **** **** $2");
            case EMAIL -> value.replaceAll("(.).+(@.+)", "$1***$2");
        };
    }
}
```

## 场景四：操作审计

记录"谁在什么时间对什么数据做了什么操作"，满足合规要求。

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface AuditLog {
    /** 操作类型 */
    String action();
    /** 模块 */
    String module();
    /** 资源ID的SpEL表达式，如 "#id" 或 "#orderDTO.orderId" */
    String resourceId() default "";
}
```

```java
@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class AuditLogAspect {

    private final AuditLogMapper auditLogMapper;
    private final ExpressionParser parser = new SpelExpressionParser();

    @AfterReturning(pointcut = "@annotation(auditLog)", returning = "result")
    public void recordAudit(JoinPoint jp, AuditLog auditLog, Object result) {
        // 获取操作人信息
        Long userId = SecurityContextHolder.getCurrentUserId();
        String userName = SecurityContextHolder.getCurrentUserName();

        // 解析 SpEL 表达式获取资源ID
        String resourceId = resolveResourceId(jp, auditLog);

        // 异步写审计日志，不影响主流程
        CompletableFuture.runAsync(() -> {
            AuditLogPO po = new AuditLogPO();
            po.setUserId(userId);
            po.setUserName(userName);
            po.setModule(auditLog.module());
            po.setAction(auditLog.action());
            po.setResourceId(resourceId);
            po.setClientIp(getClientIp());
            po.setCreateTime(LocalDateTime.now());
            auditLogMapper.insert(po);
        }, auditExecutor);
    }

    private String resolveResourceId(JoinPoint jp, AuditLog auditLog) {
        if (StringUtils.isBlank(auditLog.resourceId())) return null;
        try {
            // 解析方法参数名和值
            MethodSignature ms = (MethodSignature) jp.getSignature();
            String[] paramNames = ms.getParameterNames();
            Object[] args = jp.getArgs();

            EvaluationContext context = new StandardEvaluationContext();
            for (int i = 0; i < paramNames.length; i++) {
                context.setVariable(paramNames[i], args[i]);
            }
            Expression exp = parser.parseExpression(auditLog.resourceId());
            return exp.getValue(context, String.class);
        } catch (Exception e) {
            return null;
        }
    }
}
```

使用：

```java
@AuditLog(module = "订单管理", action = "取消订单", resourceId = "#id")
@PostMapping("/api/order/{id}/cancel")
public Result<Void> cancelOrder(@PathVariable Long id,
                                 @RequestBody CancelReason reason) {
    orderService.cancel(id, reason);
    return Result.ok(null);
}
```

## 场景五：分布式锁 AOP

防止接口被重复提交或并发操作。

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface DistributedLock {
    /** 锁的 key（SpEL 表达式） */
    String key();
    /** 等待获取锁的时间（秒） */
    int waitTime() default 3;
    /** 锁的持有时间（秒） */
    int leaseTime() default 30;
    /** 获取锁失败时的提示 */
    String message() default "操作正在进行中，请勿重复提交";
}
```

```java
@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class DistributedLockAspect {

    private final RedissonClient redissonClient;
    private final ExpressionParser parser = new SpelExpressionParser();

    @Around("@annotation(distributedLock)")
    public Object around(ProceedingJoinPoint pjp,
                         DistributedLock distributedLock) throws Throwable {
        String lockKey = "lock:" + resolveKey(pjp, distributedLock);
        RLock lock = redissonClient.getLock(lockKey);

        boolean acquired = false;
        try {
            acquired = lock.tryLock(
                distributedLock.waitTime(),
                distributedLock.leaseTime(),
                TimeUnit.SECONDS);

            if (!acquired) {
                throw new BizException(409, distributedLock.message());
            }

            return pjp.proceed();
        } finally {
            // 坑：只有当前线程持有的锁才能释放
            if (acquired && lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}
```

使用：

```java
// 防止同一个订单被重复支付
@DistributedLock(key = "'pay:' + #orderId", waitTime = 0, message = "支付处理中")
@PostMapping("/api/order/{orderId}/pay")
public Result<PayResult> pay(@PathVariable Long orderId,
                              @RequestBody PayRequest request) {
    return Result.ok(orderService.pay(orderId, request));
}
```

## AOP 的注意事项

1. **切面执行顺序**：多个切面同时作用时，用 `@Order` 控制顺序。值越小越先执行。权限校验应该在日志记录之前（`@Order(1)` vs `@Order(10)`）。

2. **切面的性能影响**：AOP 本身性能损耗很小（纳秒级），但如果切面里做了反射、序列化等操作，要注意累积效应。我们的日志切面在高 QPS 场景下把序列化改成了异步。

3. **同一个类内调用不走代理**：这是 Spring AOP 最大的"坑"，前面已经提过。实在避免不了的话，用 `AopContext.currentProxy()` 或拆分到不同的 Bean。

4. **测试困难**：AOP 切面的逻辑对单元测试不可见，需要用集成测试验证切面行为。我们用 `spring-boot-starter-test` + `@SpringBootTest` 来测试切面。
