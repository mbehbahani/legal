# `/understand-chat` Sample — Hybrid Retrieval Query

**Query:** How does hybrid retrieval work — what is the BM25 + dense fusion strategy?

---

## How Hybrid Retrieval Works

The core concept is captured in `concept:hybrid-retrieval` (layer: **Architecture & Design**):

> *"Parallel retrieval using BM25 (Dutch analyzer, top-100) and Cohere dense embeddings (embed-multilingual-v3, 1024-dim, top-100) fused via Reciprocal Rank Fusion (k=60) to produce a post-RRF top-60 candidate set, then reranked by Cohere rerank-v3-5:0 to top-8 for generation context."*

### The 4-stage top-K cascade

Defined in `design/module-1-2-retrieval.md` and tested in `tests/test_hybrid_retrieval.py`:

```
BM25 → top-100
Dense (Cohere embed-multilingual-v3, 1024-dim) → top-100
          ↓ RRF fusion (k = 60)
         top-60 merged candidates
          ↓ Cohere rerank-v3-5:0 (via Bedrock)
         top-8 → generation context
```

### What each stage does

| Stage | What happens | Why |
|---|---|---|
| **BM25** | Dutch-language analyzer, exact-term matching | Catches precise statute references (article numbers, ECLI codes, tax-year figures) |
| **Dense k-NN** | Cohere multilingual embeddings, HNSW ANN search | Catches semantic similarity — paraphrased queries, related concepts |
| **RRF (k=60)** | Reciprocal Rank Fusion: score = Σ 1/(k + rank_i) for each candidate across both lists | Merges the two ranked lists without needing calibrated scores — robust to score scale differences |
| **Cohere rerank-v3-5:0** | Cross-encoder reranker over top-60, collapses to top-8 | Most expensive step but highest precision — the reranker reads query + chunk together |

### Special routing: ECLI exact-match

`Present/module-2-retrieval.md` adds a detail not in the concept node — an **adaptive regex router** runs before the cascade:

- If the query contains an ECLI identifier (e.g. `ECLI:NL:RBZWB:2024:...`), it is routed to **ECLI exact-match lookup** first, bypassing BM25/dense entirely for that document
- This guarantees citation lookup is always exact, not approximate

### RBAC intersection point

RBAC is enforced *inside* the dense retrieval step, not after. OpenSearch's `efficient_filter` pre-computes a BitSet of allowed document IDs before HNSW traversal begins, so FIOD-classified chunks are invisible to the ANN walk entirely. This means the top-100 dense candidates are already access-controlled before RRF sees them.

### Where to look in the codebase

| File | What it contains |
|---|---|
| `design/module-1-2-retrieval.md` | Full design: chunking → index schema → hybrid query → reranking |
| `Present/module-2-retrieval.md` | Concise reference: exact k values, ECLI router, reranker latency budget |
| `tests/test_hybrid_retrieval.py` | Validates: RRF correctness, ECLI boosting, nDCG@5 improvement after reranking, top-K sizes |
| `tests/conftest.py` | `MockRAGClient` — deterministic simulator that replays the cascade without live Bedrock calls |
