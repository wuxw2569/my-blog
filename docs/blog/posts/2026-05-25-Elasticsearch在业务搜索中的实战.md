---
title: Elasticsearch在业务搜索中的实战
date: 2016-11-21
tags: 数据, Elasticsearch, 搜索引擎, 全文检索
summary: 从索引设计到深翻页优化，分享中小厂在Elasticsearch业务搜索场景中的实战经验，包括分词器选择和MySQL数据同步方案。
author: ai-helper
---

## 问题场景

我们的商品搜索原来直接用 MySQL 的 `LIKE '%关键词%'`，结果随着商品数到50万+，搜索接口RT超过3s，而且完全不支持模糊匹配、拼音搜索、相关性排序这些基本功能。

产品经理天天吐槽："用户搜'苹果手机'，出来的全是带'苹果'两个字的配件。"

是时候上 Elasticsearch 了。

## 分析思路

### 1. 索引设计：不是把 MySQL 表直接映射过来

我们用了 ES 7.17（稳定版，团队不想当小白鼠上8.x）。

**商品索引 Mapping 设计**：

```json
PUT /product_index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "ik_smart_analyzer": {
          "type": "custom",
          "tokenizer": "ik_smart"
        },
        "pinyin_analyzer": {
          "type": "custom",
          "tokenizer": "keyword",
          "filter": ["pinyin_filter"]
        }
      },
      "filter": {
        "pinyin_filter": {
          "type": "pinyin",
          "keep_full_pinyin": true,
          "keep_joined_full_pinyin": true,
          "keep_original": true
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "product_id": { "type": "long" },
      "title": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
        "fields": {
          "pinyin": {
            "type": "text",
            "analyzer": "pinyin_analyzer"
          },
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "category_id": { "type": "integer" },
      "brand_id": { "type": "integer" },
      "price": { "type": "scaled_float", "scaling_factor": 100 },
      "sales_count": { "type": "integer" },
      "status": { "type": "byte" },
      "create_time": { "type": "date" }
    }
  }
}
```

**设计要点**：

- `title` 字段同时设置了 `ik_smart` 分词和 `pinyin` 子字段，支持中文分词和拼音搜索
- `keyword` 子字段用于精确匹配（如品牌筛选）
- `price` 用 `scaled_float` 而不是 `float`，避免浮点精度问题
- **不要把所有 MySQL 字段都映射过来**，ES 只存搜索和排序需要的字段

### 2. 分词器选择：ik_smart vs ik_max_word

这是个高频问题。简单说：

- `ik_max_word`：最细粒度分词。"苹果手机" -> ["苹果", "手机", "苹果手机"]
- `ik_smart`：粗粒度分词。"苹果手机" -> ["苹果手机"]

**我们的选择**：

- **索引时用 `ik_max_word`**：尽可能多地分词，增加被搜索到的概率
- **搜索时用 `ik_smart`**：用户搜索时用粗粒度，避免匹配太多无关结果

```json
"title": {
  "type": "text",
  "analyzer": "ik_max_word",
  "search_analyzer": "ik_smart"
}
```

**自定义词典**：电商领域有大量专业词汇，`ik` 默认词典不够。我们在 `/elasticsearch/config/analysis-ik/my.dic` 中添加了行业词汇：

```
无线蓝牙耳机
真无线降噪
速干面料
除螨仪
```

### 3. 搜索查询构建

```java
@Service
public class ProductSearchService {

    @Autowired
    private RestHighLevelClient client;

    public SearchResult search(ProductSearchRequest request) {
        SearchRequest searchRequest = new SearchRequest("product_index");
        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();

        BoolQueryBuilder boolQuery = QueryBuilders.boolQuery();

        // 关键词搜索：title 和 title.pinyin 都要搜
        if (StringUtils.isNotBlank(request.getKeyword())) {
            boolQuery.must(
                QueryBuilders.multiMatchQuery(request.getKeyword(),
                    "title", "title.pinyin")
                    .type(MultiMatchQueryBuilder.Type.BEST_FIELDS)
                    .operator(Operator.AND)
            );
        }

        // 分类筛选
        if (request.getCategoryId() != null) {
            boolQuery.filter(QueryBuilders.termQuery("category_id", request.getCategoryId()));
        }

        // 价格区间
        if (request.getMinPrice() != null || request.getMaxPrice() != null) {
            RangeQueryBuilder priceRange = QueryBuilders.rangeQuery("price");
            if (request.getMinPrice() != null) priceRange.gte(request.getMinPrice());
            if (request.getMaxPrice() != null) priceRange.lte(request.getMaxPrice());
            boolQuery.filter(priceRange);
        }

        // 只搜索上架商品
        boolQuery.filter(QueryBuilders.termQuery("status", 1));

        sourceBuilder.query(boolQuery);

        // 排序：综合排序（销量 + 时间权重）
        sourceBuilder.sort(SortBuilders.scoreSort());
        sourceBuilder.sort("sales_count", SortOrder.DESC);

        // 分页
        int from = (request.getPage() - 1) * request.getSize();
        sourceBuilder.from(from);
        sourceBuilder.size(request.getSize());

        searchRequest.source(sourceBuilder);
        // ... 执行查询并返回结果
    }
}
```

### 4. 深翻页问题

ES 的分页默认用 `from + size`，但当 `from` 很大时（比如第1000页，每页20条，`from=20000`），ES 需要在每个分片上排序取 `from + size` 条数据，然后在协调节点合并排序。数据量大时内存和CPU消耗惊人。

**我们的解决方案**：

**方案一：搜索场景用 scroll search（适合导出）**

```java
// 批量导出场景
SearchResponse response = client.search(searchRequest, RequestOptions.DEFAULT);
String scrollId = response.getScrollId();

while (true) {
    SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
    scrollRequest.scroll(TimeValue.timeValueMinutes(1));
    response = client.scroll(scrollRequest, RequestOptions.DEFAULT);

    if (response.getHits().getHits().length == 0) break;
    // 处理数据...
}
// 清理 scroll
ClearScrollRequest clearRequest = new ClearScrollRequest();
clearRequest.addScrollId(scrollId);
client.clearScroll(clearRequest, RequestOptions.Default);
```

**方案二：用户翻页限制在100页以内**

直接限制最大翻页深度，超过的引导用户用更精确的搜索条件。

**方案三：search_after（推荐用于深度分页）**

```java
// 第一次查询
sourceBuilder.size(20);
sourceBuilder.sort("sales_count", SortOrder.DESC);
sourceBuilder.sort("_id", SortOrder.ASC);  // tiebreaker

// 后续查询，用上一页最后一条数据的sort值
Object[] lastSortValues = new Object[]{lastSalesCount, lastId};
sourceBuilder.searchAfter(lastSortValues);
```

## 具体实现

### MySQL 到 ES 的数据同步

这是整个方案中最容易出问题的环节。我们尝试了三种方案：

**方案一：同步双写（已弃用）**

```java
@Transactional
public void createProduct(Product product) {
    productMapper.insert(product);
    // 直接写 ES
    elasticsearchTemplate.save(product);
}
```

问题：写 ES 失败怎么办？重试的话 MySQL 事务已提交。不重试的话数据不一致。耦合太紧。

**方案二：Canal + MQ 异步同步（当前方案）**

```
MySQL binlog -> Canal Server -> RocketMQ -> ES同步服务 -> Elasticsearch
```

```java
@Component
@RocketMQMessageListener(
    topic = "TOPIC_ES_PRODUCT_SYNC",
    consumerGroup = "CG_ES_SYNC"
)
public class EsSyncConsumer implements RocketMQListener<ProductChangeEvent> {

    @Override
    public void onMessage(ProductChangeEvent event) {
        switch (event.getEventType()) {
            case INSERT:
            case UPDATE:
                Product product = productMapper.selectById(event.getProductId());
                if (product != null) {
                    IndexRequest request = new IndexRequest("product_index")
                        .id(product.getId().toString())
                        .source(convertToMap(product));
                    client.index(request, RequestOptions.DEFAULT);
                }
                break;
            case DELETE:
                DeleteRequest deleteRequest = new DeleteRequest("product_index")
                    .id(event.getProductId().toString());
                client.delete(deleteRequest, RequestOptions.DEFAULT);
                break;
        }
    }
}
```

**方案三：定时全量重建（兜底方案）**

每天凌晨用定时任务全量重建索引，保证最终一致性：

```java
@Scheduled(cron = "0 0 3 * * ?")
public void rebuildProductIndex() {
    // 创建新索引 product_index_v2
    // 全量导入数据
    // 别名切换：product_index 指向 v2
    // 删除旧索引 v1
}
```

## 踩坑总结

1. **Mapping 设计要提前规划好**。一旦建立，修改字段类型只能 reindex。我们有次把 `price` 设成 `text` 类型，排序全是字典序，返工了一天。
2. **ik_max_word 和 ik_smart 搭配使用**。索引时细粒度、搜索时粗粒度，这是业界验证过的最佳实践。
3. **自定义词典必须维护**。不加行业术语，分词效果一塌糊涂。我们每周从搜索日志中提取新词更新词典。
4. **深翻页问题不要忽视**。上线前测试都是小数据量，翻页很顺畅。上线后数据量上来，第50页就开始超时。
5. **数据同步方案首选 Canal + MQ**。同步双写耦合太紧，定时同步延迟太高，Canal 是最佳平衡点。
6. **ES 不适合做主存储**。它是搜索引擎，不是数据库。数据的源头永远是 MySQL，ES 只是索引层。
