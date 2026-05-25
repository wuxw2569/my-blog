---
title: Spring AI实现RAG知识库检索增强
date: 2026-06-14
tags: AI, Spring AI, RAG, 知识库, 向量检索, Milvus
summary: 用 Spring AI 实现 RAG 检索增强生成，从文档加载到向量存储再到 Prompt 组装的完整落地方案。
author: ai-helper
---

## 问题场景

客服系统接入大模型后，有个明显的问题：模型不知道我们公司的产品信息、售后政策、常见问题。纯靠模型的通用知识，回答经常"一本正经地胡说八道"。

我们需要一个方案，把公司的文档知识喂给模型。最直觉的做法是把文档塞到 Prompt 里，但公司文档库有几百篇，全塞进去 Token 爆炸，而且检索效率极低。

RAG（Retrieval Augmented Generation，检索增强生成）就是解决这个问题的标准方案：先从知识库里检索出跟问题相关的文档片段，再把这些片段作为上下文交给模型回答。

## 分析思路

RAG 的核心流程分三步：

1. **离线索引**：加载文档 -> 文本分割 -> 生成 Embedding -> 存入向量库
2. **在线检索**：用户问题 -> 生成问题 Embedding -> 向量相似度搜索 -> 取回相关片段
3. **生成回答**：把检索结果 + 用户问题组装成 Prompt -> 调用模型生成回答

Spring AI 对这三个步骤都有封装，但用起来还是有不少需要自己处理的地方。

## 具体实现

### 第一步：依赖配置

```xml
<!-- 文档解析 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-tika-document-reader</artifactId>
</dependency>

<!-- 文本分割 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-core</artifactId>
</dependency>

<!-- Milvus 向量库 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-milvus-store-spring-boot-starter</artifactId>
</dependency>
```

```yaml
# application.yml
spring:
  ai:
    vectorstore:
      milvus:
        host: ${MILVUS_HOST:localhost}
        port: ${MILVUS_PORT:19530}
        collection-name: knowledge_base
        index-type: IVF_FLAT
        metric-type: COSINE
        dimension: 1536
```

### 第二步：文档加载与分割

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class DocumentIndexService {

    private final VectorStore vectorStore;

    /**
     * 加载并索引文档目录下的所有文件
     * 支持 PDF、Word、TXT、Markdown 等格式
     */
    public void indexDocuments(String directoryPath) {
        log.info("【文档索引开始】目录: {}", directoryPath);
        File dir = new File(directoryPath);
        if (!dir.exists() || !dir.isDirectory()) {
            throw new IllegalArgumentException("目录不存在: " + directoryPath);
        }

        // 使用 Tika 解析各种文档格式
        List<Document> documents = new ArrayList<>();
        for (File file : Objects.requireNonNull(dir.listFiles())) {
            try {
                // TikaDocumentReader 自动识别文件类型
                TikaDocumentReader reader = new TikaDocumentReader(new FileSystemResource(file));
                List<Document> docs = reader.get();
                // 给每个文档打上元数据标签，方便后续过滤
                docs.forEach(doc -> {
                    doc.getMetadata().put("source", file.getName());
                    doc.getMetadata().put("indexTime", Instant.now().toString());
                });
                documents.addAll(docs);
                log.info("【文档加载】文件: {}, 片段数: {}", file.getName(), docs.size());
            } catch (Exception e) {
                log.warn("【文档加载失败】文件: {}, 错误: {}", file.getName(), e.getMessage());
            }
        }

        // 文本分割
        TokenTextSplitter splitter = new TokenTextSplitter(
                800,   // 每段最大 token 数
                200,   // 重叠 token 数（保证上下文连贯）
                5,     // 最小每段 token 数
                10000, // 最大 token 数
                true   // 保留分隔符
        );
        List<Document> chunks = splitter.apply(documents);
        log.info("【文本分割完成】原始文档: {} 篇, 分割后: {} 个片段", documents.size(), chunks.size());

        // 写入向量库（自动生成 Embedding）
        vectorStore.add(chunks);
        log.info("【文档索引完成】已写入向量库");
    }
}
```

**踩坑点**：`TokenTextSplitter` 的 chunk size 设置很关键。太大了检索结果不够精确，太小了上下文不完整。我们经验是 500-1000 token 比较合适，看文档类型。结构化文档（如 FAQ）可以小一点，叙述性文档（如产品手册）要大一点。

### 第三步：检索服务

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class KnowledgeSearchService {

    private final VectorStore vectorStore;

    /**
     * 检索与问题相关的知识片段
     * @param query 用户问题
     * @param topK 返回的最大片段数
     * @param threshold 相似度阈值（0-1），低于此值的结果不返回
     */
    public List<Document> search(String query, int topK, double threshold) {
        log.info("【知识检索】查询: {}, topK: {}, 阈值: {}", query, topK, threshold);

        SearchRequest request = SearchRequest.query(query)
                .withTopK(topK)
                .withSimilarityThreshold(threshold);

        List<Document> results = vectorStore.similaritySearch(request);

        log.info("【检索完成】命中 {} 个片段", results.size());
        results.forEach(doc -> {
            log.debug("【检索结果】来源: {}, 相似度: {}, 内容摘要: {}",
                    doc.getMetadata().get("source"),
                    doc.getScore(),
                    doc.getText().substring(0, Math.min(100, doc.getText().length())));
        });

        return results;
    }

    /**
     * 带过滤条件的检索
     * 比如只检索特定来源的文档
     */
    public List<Document> searchWithFilter(String query, String sourceFilter, int topK) {
        SearchRequest request = SearchRequest.query(query)
                .withTopK(topK)
                .withSimilarityThreshold(0.7)
                .withFilterExpression("source == '" + sourceFilter + "'");

        return vectorStore.similaritySearch(request);
    }
}
```

### 第四步：Prompt 组装与问答

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class RagChatService {

    private final ChatModel chatModel;
    private final KnowledgeSearchService searchService;

    private static final String RAG_SYSTEM_PROMPT = """
            你是一个专业的客服助手。请基于以下知识库内容回答用户的问题。
            
            规则：
            1. 只根据提供的知识内容回答，不要编造信息
            2. 如果知识库中没有相关信息，请明确告知用户"根据现有知识库暂无法回答"
            3. 回答要简洁准确，必要时可以分点说明
            4. 如果用户的问题模糊，可以先确认再回答
            
            ---知识库内容---
            {context}
            ---知识库内容结束---
            """;

    /**
     * RAG 问答：检索 + 生成
     */
    public String chat(String userMessage) {
        // 第一步：检索相关知识
        List<Document> relevantDocs = searchService.search(userMessage, 5, 0.6);

        // 第二步：组装上下文
        String context = relevantDocs.stream()
                .map(doc -> String.format("【来源: %s】%s",
                        doc.getMetadata().get("source"), doc.getText()))
                .collect(Collectors.joining("\n\n"));

        if (context.isEmpty()) {
            log.warn("【RAG】未检索到相关内容，使用通用回答");
            context = "（暂无相关知识库内容）";
        }

        // 第三步：组装 Prompt 并调用模型
        String systemPrompt = RAG_SYSTEM_PROMPT.replace("{context}", context);

        Prompt prompt = new Prompt(List.of(
                new SystemMessage(systemPrompt),
                new UserMessage(userMessage)
        ));

        log.info("【RAG问答】用户: {}, 检索片段: {}, 上下文长度: {}",
                userMessage, relevantDocs.size(), context.length());

        ChatResponse response = chatModel.call(prompt);
        String answer = response.getResult().getOutput().getContent();

        log.info("【RAG回答完成】Token使用: prompt={}, completion={}",
                response.getMetadata().getUsage().getPromptTokens(),
                response.getMetadata().getUsage().getCompletionTokens());

        return answer;
    }
}
```

### 第五步：定时重建索引

```java
@Component
@Slf4j
@RequiredArgsConstructor
public class IndexScheduler {

    private final DocumentIndexService indexService;

    /**
     * 每天凌晨 2 点重建索引
     * 也可以配合文件监听做增量更新
     */
    @Scheduled(cron = "0 0 2 * * ?")
    public void rebuildIndex() {
        log.info("【定时任务】开始重建知识库索引");
        try {
            indexService.indexDocuments("/data/knowledge-docs");
            log.info("【定时任务】索引重建完成");
        } catch (Exception e) {
            log.error("【定时任务】索引重建失败", e);
        }
    }
}
```

## 踩坑总结

1. **Embedding 模型的选择很关键**：DashScope 提供了 `text-embedding-v2` 模型，1536 维度。如果用的是其他向量库（比如 Redis 的 dim 是 768），维度要跟模型对齐，否则存不进去。

2. **文本分割策略要反复调试**：我们一开始用固定长度分割，结果把一句话拆到两个片段里，检索出来的内容断断续续。后来改成按段落分割 + 重叠窗口，效果好了很多。

3. **相似度阈值不能太高**：设 0.8 以上的话，很多相关但表述不同的文档检索不到。我们最终设的 0.6，配合 topK=5 再让模型自己判断哪些信息有用。

4. **Milvus 的索引类型选 IVF_FLAT**：IVF_SQ8 虽然省内存，但精度损失在我们的知识库规模下（几万条）不太值得。如果数据量到百万级再考虑量化索引。

5. **Prompt 中的指令很重要**：不加"只根据提供的知识内容回答"这句话，模型经常会忽略检索结果，用自己的知识回答。加了之后准确率明显提升。

6. **文档更新的时效性**：知识库文档经常更新，如果用定时任务重建索引，中间会有时间窗口用的是旧知识。生产环境建议配合文件监听做增量更新，或者通过 API 手动触发。
