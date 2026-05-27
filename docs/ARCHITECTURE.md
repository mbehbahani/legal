# Architecture

This file is a navigation index. Authoritative content lives in [design/FINAL-rag-architecture.md](../design/FINAL-rag-architecture.md); the four module docs below are deep dives. Cross-cutting structural facts came from [graphify-out/GRAPH_REPORT.md](../graphify-out/GRAPH_REPORT.md).

## The four modules

### Module 1 + 2 — Ingestion & Retrieval — [design/module-1-2-retrieval.md](../design/module-1-2-retrieval.md)
Chunking strategy, hierarchical metadata schema, OpenSearch HNSW config + quantization, hybrid (BM25 + dense) fusion, Cohere reranker, parent-document retrieval at generation time.

### Module 3 — Agentic RAG — [design/module-3-agentic.md](../design/module-3-agentic.md)
Query transformation (decomposition + HyDE routing rule), Corrective-RAG (CRAG) state machine implemented in LangGraph, retrieval grader prompt, fallback policy, citation verifier, per-node latency budget.

### Module 4 — Ops & Security — [design/module-4-ops-security.md](../design/module-4-ops-security.md)
Semantic cache (Redis), RBAC three-layer defense-in-depth with OpenSearch `efficient_filter`, CI/CD promotion gates, OpenTelemetry span hierarchy, Bedrock cost dashboard.

## Cross-cutting facts (from the graph)

### God nodes (most-connected abstractions)
| Node | Edges | Role |
|---|---|---|
| `UserContext` | 49 | Identity/role envelope threaded through every test and pipeline stage |
| `ChunkMeta` | 45 | The hierarchical-metadata record around each retrieved chunk |
| `MockRAGClient` | 42 | Deterministic stub used by the evaluation suite |
| `HaikuJudge` | 30 | Bedrock-Haiku LLM-as-judge wrapper |
| `RAGResponse` | 25 | The contract the full pipeline emits |
| `TelemetrySink` | 22 | In-memory span collector for observability tests |

If you change any of these, expect wide blast radius. Run `graphify affected "<node>"` to enumerate downstream callers before editing.

### Load-bearing security decision
RBAC must run **inside HNSW traversal** via OpenSearch `efficient_filter` — post-filtering leaks via empty-set + timing side channels. See module 4 §3.2 ("Mathematical Proof: Why Post-Filtering Leaks").

### Cache invariants
The semantic cache key is bound to `(query_embedding, role, tax_year)`. A role-blind or year-blind key is a cache-poisoning vector — see module 4 §2.2 ("WARNING — The Cache Must Not Be Role-Blind") and the worked tests in [tests/test_semantic_cache.py](../tests/test_semantic_cache.py).

## Diagrams
The design docs embed Mermaid diagrams for the CRAG state machine, the RBAC pre-filter pipeline, and the OTel span hierarchy. The graph at [graphify-out/graph.html](../graphify-out/graph.html) is the live interactive view of the repo's symbol-level relationships.
