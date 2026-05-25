---
title: Spring AI流式输出SSE实现聊天界面
date: 2026-05-25
tags: AI, Spring AI, SSE, 流式输出, StreamingChatClient
summary: 用 Spring AI 的流式输出能力实现 SSE 推送，打造打字机效果的聊天体验，包含前端对接和 Token 统计。
author: ai-helper
---

## 问题场景

聊天接口上线后，用户反馈体验很差：一个问题发出去，要等 3-5 秒才返回完整答案，期间页面一片空白，不知道在干什么。

这是同步调用的典型问题。大模型生成回答是一个 token 一个 token 往外出的，同步接口必须等全部生成完才返回。解决办法就是流式输出（Streaming）：模型生成一个 token 就立刻推送给前端，前端实时展示，形成"打字机"效果。

## 分析思路

Spring AI 支持两种调用方式：
- `chatClient.call()` -- 同步，等完整结果
- `chatClient.stream()` -- 流式，逐 token 返回

后端用 SSE（Server-Sent Events）推送，前端用 EventSource 或 fetch + ReadableStream 接收。

技术要点：
1. 后端 `Flux<String>` 返回 SSE 流
2. 前端实时渲染并处理 Markdown
3. Token 统计和超时处理

## 具体实现

### 后端：流式接口

```java
@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
@Slf4j
public class StreamChatController {

    private final ChatClient chatClient;

    /**
     * 流式对话接口
     * produces = "text/event-stream" 是 SSE 的标准 Content-Type
     */
    @PostMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> streamChat(@RequestBody ChatRequest request) {
        log.info("【流式对话】用户输入: {}", request.message());

        return chatClient.prompt()
                .user(request.message())
                .stream()
                .chatResponse()
                // 提取每个 chunk 的文本内容
                .mapNotNull(response -> {
                    var output = response.getResult().getOutput();
                    if (output != null && output.getContent() != null) {
                        return output.getContent();
                    }
                    return null;
                })
                // 过滤空内容
                .filter(StringUtils::hasText)
                // 包装成 SSE 事件
                .map(content -> ServerSentEvent.<String>builder()
                        .data(content)
                        .event("message")
                        .build())
                // 发送完成事件
                .concatWith(Flux.just(
                        ServerSentEvent.<String>builder()
                                .data("[DONE]")
                                .event("done")
                                .build()
                ))
                .doOnComplete(() -> log.info("【流式对话完成】"))
                .doOnError(e -> log.error("【流式对话异常】", e))
                .onErrorResume(e -> Flux.just(
                        ServerSentEvent.<String>builder()
                                .data("抱歉，生成回答时出现错误: " + e.getMessage())
                                .event("error")
                                .build()
                ));
    }

    /**
     * 流式对话 + 完整 Token 统计
     * 通过 ChatResponse 的 metadata 获取 token 用量
     */
    @PostMapping(value = "/stream-with-stats", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> streamChatWithStats(@RequestBody ChatRequest request) {
        log.info("【流式对话+统计】用户输入: {}", request.message());

        // 使用 AtomicReference 收集最后一次 response 的 metadata
        AtomicReference<Usage> lastUsage = new AtomicReference<>();
        StringBuilder fullContent = new StringBuilder();

        return chatClient.prompt()
                .user(request.message())
                .stream()
                .chatResponse()
                .map(response -> {
                    var output = response.getResult().getOutput();
                    String content = (output != null && output.getContent() != null)
                            ? output.getContent() : "";
                    fullContent.append(content);

                    // 保存最后一次的 usage 信息
                    if (response.getMetadata() != null
                            && response.getMetadata().getUsage() != null) {
                        lastUsage.set(response.getMetadata().getUsage());
                    }

                    return ServerSentEvent.<String>builder()
                            .data(content)
                            .event("message")
                            .build();
                })
                .concatWith(Flux.fromCallable(() -> {
                    // 发送统计信息
                    Usage usage = lastUsage.get();
                    String stats = String.format(
                            "{\"promptTokens\":%d,\"completionTokens\":%d,\"totalTokens\":%d}",
                            usage != null ? usage.getPromptTokens() : 0,
                            usage != null ? usage.getCompletionTokens() : 0,
                            usage != null ? usage.getTotalTokens() : 0);
                    return ServerSentEvent.<String>builder()
                            .data(stats)
                            .event("stats")
                            .build();
                }))
                .concatWith(Flux.just(
                        ServerSentEvent.<String>builder()
                                .data("[DONE]")
                                .event("done")
                                .build()
                ));
    }

    public record ChatRequest(String message) {}
}
```

### 后端：超时和背压处理

```java
@RestControllerAdvice
public class StreamExceptionHandler {

    /**
     * 流式接口的超时配置
     * 放在 WebFlux 的配置类中
     */
    @Configuration
    public static class StreamConfig {

        @Bean
        public WebFluxConfigurer webFluxConfigurer() {
            return new WebFluxConfigurer() {
                @Override
                public void configureHttpMessageCodecs(ServerCodecConfigurer configurer) {
                    // 增大 SSE 缓冲区
                    configurer.defaultCodecs().maxInMemorySize(1024 * 1024);
                }
            };
        }
    }
}
```

对于超时，可以在 ChatClient 层面加 timeout：

```java
// 在 ChatClient 配置中加超时
@Bean
public ChatClient chatClient(ChatModel chatModel) {
    return ChatClient.builder(chatModel)
            .defaultSystem("你是客服助手")
            .defaultOptions(DashScopeChatOptions.builder()
                    .withModel("qwen-plus")
                    .withMaxTokens(2048)
                    .build())
            .build();
}
```

DashScope 的流式接口本身有超时限制，如果模型生成时间过长（超过 60 秒），连接会断开。前端需要处理这种情况。

### 前端：对接 SSE

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>AI 客服</title>
    <style>
        :root {
            --primary: #1677ff;
            --bg: #f5f5f5;
            --card-bg: #fff;
            --text: #333;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; background: var(--bg); }
        .chat-container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .message { margin: 12px 0; padding: 12px 16px; border-radius: 8px; max-width: 80%; }
        .user-msg { background: var(--primary); color: #fff; margin-left: auto; }
        .ai-msg { background: var(--card-bg); border: 1px solid #e8e8e8; }
        .input-area { display: flex; gap: 8px; margin-top: 20px; }
        .input-area input { flex: 1; padding: 12px; border: 1px solid #d9d9d9; border-radius: 8px; font-size: 14px; }
        .input-area button { padding: 12px 24px; background: var(--primary); color: #fff; border: none; border-radius: 8px; cursor: pointer; }
        .stats { font-size: 12px; color: #999; margin-top: 4px; }
        .cursor-blink::after { content: '▊'; animation: blink 0.8s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="chat-container" id="chatBox">
        <div id="messages"></div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="输入消息..." 
                   onkeydown="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('messages');
        const userInput = document.getElementById('userInput');

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            // 显示用户消息
            appendMessage('user', text);
            userInput.value = '';

            // 创建 AI 消息容器（带光标闪烁效果）
            const aiDiv = appendMessage('ai', '');
            aiDiv.classList.add('cursor-blink');

            try {
                const response = await fetch('/api/chat/stream-with-stats', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                let fullText = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop(); // 保留不完整的行

                    let eventType = '';
                    for (const line of lines) {
                        if (line.startsWith('event:')) {
                            eventType = line.substring(6).trim();
                        } else if (line.startsWith('data:')) {
                            const data = line.substring(5).trim();
                            if (data === '[DONE]') {
                                aiDiv.classList.remove('cursor-blink');
                                continue;
                            }
                            if (eventType === 'message') {
                                fullText += data;
                                aiDiv.textContent = fullText;
                                scrollToBottom();
                            } else if (eventType === 'stats') {
                                const stats = JSON.parse(data);
                                const statsDiv = document.createElement('div');
                                statsDiv.className = 'stats';
                                statsDiv.textContent = `Token: ${stats.totalTokens} (输入${stats.promptTokens} + 输出${stats.completionTokens})`;
                                aiDiv.appendChild(statsDiv);
                            } else if (eventType === 'error') {
                                aiDiv.textContent = '❌ ' + data;
                                aiDiv.classList.remove('cursor-blink');
                            }
                        }
                    }
                }
            } catch (err) {
                aiDiv.textContent = '❌ 连接失败: ' + err.message;
                aiDiv.classList.remove('cursor-blink');
            }
        }

        function appendMessage(role, text) {
            const div = document.createElement('div');
            div.className = 'message ' + (role === 'user' ? 'user-msg' : 'ai-msg');
            div.textContent = text;
            messagesDiv.appendChild(div);
            scrollToBottom();
            return div;
        }

        function scrollToBottom() {
            document.getElementById('chatBox').scrollTop = 
                document.getElementById('chatBox').scrollHeight;
        }
    </script>
</body>
</html>
```

## 踩坑总结

1. **SSE 连接被 Nginx 超时断开**：Nginx 默认的 proxy_read_timeout 是 60 秒，如果模型生成较慢，连接会断。配置 `proxy_read_timeout 300s;` 和 `proxy_buffering off;`。

2. **`text/event-stream` 不能有 BOM**：有些 HTTP 客户端库会自动加 BOM 头，导致前端解析 SSE 失败。Spring MVC 默认不会加，但如果用了自定义的 MessageConverter 要注意。

3. **前端 buffer 处理**：SSE 的 data 可能被拆成多个 chunk 发送，前端必须做 buffer 拼接。特别是中文，一个 UTF-8 字符可能被拆到两个 chunk 里，直接 decode 会乱码。用 `decoder.decode(value, { stream: true })` 可以解决。

4. **Token 统计时机**：流式响应中，token 用量信息通常在最后一个 chunk 的 metadata 里。但有些实现是通过独立的 usage chunk 发送的。DashScope 是在最后一批返回。

5. **取消生成**：用户可能在模型还在生成时就关掉页面或点"停止"。后端需要处理连接断开事件，及时停止模型生成，否则还在继续消耗 Token：

```java
// 在 Flux 中加 takeUntilOther 处理取消
.doOnCancel(() -> log.info("【流式对话】客户端断开连接，停止生成"))
```

6. **并发流式连接数**：每个流式连接都会占用一个线程（或一个 Reactor subscription），大量并发时要注意线程池大小。Spring WebFlux 的默认线程数是 CPU 核心数，如果流式接口很多，可能需要调大。

7. **Markdown 渲染**：我们示例里用的是纯文本展示，实际项目中通常需要支持 Markdown。但流式渲染 Markdown 有个问题：代码块（```）可能只收到一半，直接渲染会错乱。需要在前端做一个"未闭合标签检测"的处理。
