# Plan — RAG Retrieval Architect (Modules 1 & 2)

## 1. Deliverables
- **File:** `d:\AWS\Legal\design\module-1-2-retrieval.md`
- **Outline:** 1.1 Chunking (legislation vs. case law) with LlamaIndex pseudo-code; 1.2 Hierarchical metadata schema; 1.3 Vector DB selection + sharding/mmap plan; 1.4 HNSW + quantization with memory math (~20M x 1024-d); 1.5 OOM/indexing mitigations; 2.1 Hybrid BM25+dense fusion; 2.2 Reranker selection + sovereignty note; 2.3 Top-K cascade and < 1.5s TTFT latency budget.

## 2. Key design decisions (current leaning)
1. **Chunking** — Structure-aware split on Article/Paragraph/Sub for legislation; semantic-section split for case law (header / facts / considerations / ruling). Parent-document retrieval: 256-token leaf chunks, 1500-token parent passed to LLM. *Why:* preserves cite granularity while keeping context.
2. **Metadata schema** — `doc_id, doc_type, eli_or_ecli, article, paragraph, sub, effective_date, superseded_by, classification, jurisdiction, language, parent_chunk_id, hierarchy_path, hash`. *Why:* satisfies citation, RBAC pre-filter, and point-in-time tax-law retrieval.
3. **Vector store** — **Amazon OpenSearch Service** (Lucene engine, k-NN HNSW with `efficient_filter`). *Why:* the RBAC pre-filter runs *inside* HNSW traversal — mathematically safe vs. post-filter leak. Native BM25 in the same engine eliminates a separate sparse service. AWS-managed fits the AWS-resident stack.
4. **HNSW** — `m=32`, `ef_construction=256`, `ef_search=128` (tunable to 64 under load; OpenSearch spelling is `ef_construction`). *Why:* recall ≥0.95 at 20M points, 1024-dim Cohere embeddings.
5. **Quantization** — OpenSearch **FP16 scalar quantization** (2.13+) on hot tier; evaluate **binary quantization** (2.16+) with rescore for max memory savings at 20M scale. *Why:* ~2× memory reduction with negligible recall loss; binary path explored if RAM-constrained.
6. **Embeddings** — **Cohere `embed-multilingual-v3` on Bedrock** (1024-dim, confirmed working on Dutch text). `input_type=search_document` for indexing, `search_query` for retrieval. *Why:* NL-capable, AWS-resident, no egress for FIOD content.
7. **Hybrid fusion** — OpenSearch native **`hybrid` query** with RRF via search pipeline (k=60 default). Regex router boosts BM25 when query contains ECLI/article-number patterns. *Why:* single engine; RRF is parameter-light; router catches exact-citation queries.
8. **Reranker** — **Cohere `rerank-v3-5:0` on Bedrock** (confirmed working — correctly ranked Dutch tax doc 0.88 vs off-topic 0.02). *Why:* multilingual, AWS-resident (no Cohere SaaS egress), high quality.
9. **Top-K cascade** — BM25 100, k-NN 100, RRF-fuse to 60, rerank to **top-8** for LLM context. *Why:* fits 1.5s TTFT (~80 ms hybrid query + ~250 ms Bedrock rerank + LLM prefill).

## 3. Open questions
- OpenSearch deployment shape: managed Amazon OpenSearch Service vs Serverless vs self-hosted EC2?
- Region: us-east-1 (colocate with Bedrock) vs eu-central-1 (NL data residency — needs Cohere model availability check)?
- Exact corpus size — 500k docs given; chunk count assumption 20M (~40 chunks/doc) — confirm.
- Cohere embed dimension: full 1024 or compress to 384 via `embedding_types=int8`? Affects RAM 4×.

## 4. Dependencies / handoffs
- **To mlops-security-architect (Module 4):** `classification` enum (`public | internal | fiod`) as a `keyword`-mapped field; the RBAC pre-filter uses OpenSearch `efficient_filter` clause inside the k-NN query. I will publish the exact field name, mapping, and example query DSL.
- **To agentic-rag-designer (Module 3):** citation object shape `{doc_id, doc_type, eli_or_ecli, article, paragraph, sub, effective_date, url}` returned with every chunk so the generator can emit verbatim citations.
- **To rag-evaluation-engineer:** retrieval-only metrics surface (Recall@k, MRR, nDCG) tied to the chosen K values; Bedrock model IDs and `input_type` conventions.

## 5. Estimated effort
Full module write-up: ~1,800–2,400 words, 2 pseudo-code blocks, 2 small tables (HNSW/quant memory math + latency budget). ~35–45 minutes of focused drafting.
