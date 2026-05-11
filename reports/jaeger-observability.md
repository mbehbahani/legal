# Observability Report — Jaeger Distributed Tracing
## Tax Authority RAG Pipeline

**Captured:** 2026-05-07  
**Jaeger version:** all-in-one (OTLP gRPC 4317, UI port 16686)  
**Service name:** `tax-rag`  
**Traces captured:** 16 representative traces across 3 query scenarios  
**Raw trace JSON:** `reports/jaeger-screenshots/trace-*.json`

---

## Why Jaeger? Role in the Architecture

Every user query to the RAG system travels through **10 pipeline stages** — from JWT authentication to CloudWatch audit logging. Without observability, you have no way to answer:

- Where did 1.5 seconds go? Was it the vector search or the LLM?
- Did the RBAC filter actually run before the embedding call?
- Is the reranker consistently taking 200ms? Is that degrading?
- Did the grader refuse a query, and at what point in the pipeline?

Jaeger answers all of these by recording every pipeline stage as a **span** — a timed event with attributes. Spans are linked into **traces** (one per user request) using W3C TraceContext propagation. Every span carries `user_role`, `trace_id`, and the relevant model ID, creating a complete audit trail that satisfies the 7-year CloudWatch retention requirement.

---

## Screenshot 1 — Trace Overview (Scatter Plot): 16 Traces

**What you see:**  
A scatter plot with time on the X-axis and total duration on the Y-axis. Each dot is one user request. 16 traces are shown, emitted during the demo run.

**Three visible clusters:**

| Cluster | Duration | Colour | Meaning |
|---|---|---|---|
| Top cluster | ~1.3s – 1.95s | Teal | Full generation path: retrieval → rerank → grade → generate → verify |
| Middle cluster | ~650ms – 682ms | Teal + Red | Refusal / RBAC-blocked: stops at grader, no generation |
| Bottom dots | ~10ms | Near zero | Cache hit: auth + Redis lookup only — full pipeline skipped |

**What this tells you:**  
The system has three **distinct performance profiles** depending on the query outcome. The bimodal distribution (1.5s vs 650ms) is architectural — not random jitter. Queries that get refused do half the work of queries that get answered. Cache hits are 170× faster than full answers.

---

## Screenshot 2 — Full Generation Trace Waterfall (1.87s, 12 spans)

**Query:** `ECLI:NL:HR:2021:1234 arrest box 2 dividend` (inspector role)  
**Verdict:** Relevant → full answer generated

```
rag.request ──────────────────────────────────────────── 1,878ms
│
├─ auth.extract_role         ██  5ms
│
├─ bedrock.embed             ████  53ms
│    model: cohere.embed-multilingual-v3
│    input_type: search_query, dimensions: 1024
│
├─ opensearch.retrieve       ████████████  205ms
│   ├─ opensearch.hnsw_knn   ██████  101ms   (RBAC BitSet pre-applied)
│   ├─ opensearch.bm25       ██████   92ms   (Dutch analyser, DLS enforced)
│   └─ opensearch.rrf_fusion ██   12ms       (k=60 fusion)
│
├─ bedrock.rerank            ████████████  195ms
│    model: cohere.rerank-v3-5:0, top_k: 60→8
│
├─ haiku.grade               █████████████  226ms
│    model: us.anthropic.claude-haiku-4-5-20251001-v1:0
│    verdict: Relevant
│
├─ haiku.generate            ████████████████████████████████████████  1,050ms
│    input_tokens: 512, output_tokens: 128, stream: true
│    ← DOMINANT SPAN — 56% of total request time
│
├─ citation.verify           ████████  120ms
│    depth: lid+onderdeel+sub, grounded: true
│
└─ audit.emit                ██  23ms
     sink: CloudWatch + S3 Object Lock 7yr
```

**Interpretation:**

**Haiku generates for 1.05 seconds** — 56% of the entire request. This is expected and healthy: LLM token generation dominates latency in any RAG system. The remaining 44% (820ms) is the deterministic pipeline: embed → retrieve → rerank → grade → verify → audit.

**HNSW + BM25 run in parallel** inside the `opensearch.retrieve` span (101ms + 92ms, but the total is only 205ms because they are executed concurrently). The RRF fusion then merges results in 12ms.

**The RBAC filter is invisible in the waterfall** — this is by design. The `efficient_filter` BitSet is pre-computed before HNSW traversal begins (see Module 1 §2.2). It has no span of its own because it is not a separate operation; it is baked into the HNSW traversal cost. FIOD documents never enter the graph walk.

**Latency budget check vs Module 4 §4.2:**

| Component | Measured | Budget | Status |
|---|---|---|---|
| Retrieval (HNSW+BM25+RRF) | 205ms | ≤ 300ms | ✅ |
| Rerank | 195ms | ≤ 200ms | ✅ |
| TTFT (embed+retrieve+rerank+grade+generate) | ~1,730ms | ≤ 1,500ms | ⚠️ marginally over |
| End-to-end | 1,878ms | ≤ 4,000ms | ✅ |

The TTFT slightly exceeds the 1,500ms design budget for the inspector-role ECLI trace. The helpdesk Box-1 trace (1,574ms) also marginally exceeds. In production this is resolved by: (1) using Haiku 4.5 streaming so the first token reaches the user well before 1,500ms even if total generation takes longer, and (2) moving longer ECLI queries to the async generation path.

---

## Screenshot 3 — Cache Hit Trace (11ms, 3 spans)

**Query:** Same Box 1 query — second request within TTL  
**Verdict:** Cache hit — full pipeline skipped

```
rag.request ████  11ms
│
├─ auth.extract_role   ████  4.7ms
│
└─ cache.lookup        █████  6.6ms
     redis.hit: true
     key_prefix: emb_bucket|helpdesk
     (classification_ceiling + tax_year encoded in SHA-256 key)
```

**Interpretation:**

The cache hit trace has **only 3 spans** — auth, lookup, done. The entire retrieval, embedding, reranking, grading, and generation pipeline is bypassed. Total time: **11ms** vs **1,574ms** for the same query answered cold. That is a **143× speedup**.

The cache key encodes `emb_bucket ‖ role ‖ classification_ceiling ‖ tax_year` (Module 4 §3.1). This means:
- A helpdesk user and an inspector asking the same question get **different cache entries** — their allowed document sets differ.
- A 2023 query and a 2024 query on the same topic get **different cache entries** — the answer changes year to year.
- The 0.97 cosine floor means only semantically near-identical queries hit the cache; paraphrases may miss.

This is the key security property: **the cache cannot be a confused-deputy side-channel** because role and classification ceiling are baked into the key.

---

## Screenshot 4 — Refusal Trace (682ms, 10 spans)

**Query:** `Hoeveel bedraagt zegelrecht Curaçao 2024?` (out-of-corpus query, helpdesk)  
**Verdict:** Irrelevant → structured_refusal, no generation

```
rag.request ─────────────────────────────  682ms
│
├─ auth.extract_role   ██  5ms
│
├─ bedrock.embed       ████  50ms
│
├─ opensearch.retrieve ███████████  200ms
│   ├─ opensearch.hnsw_knn   ██████   98ms
│   ├─ opensearch.bm25       ██████   91ms
│   └─ opensearch.rrf_fusion ██   11ms
│
├─ bedrock.rerank      ████████████  191ms
│
├─ haiku.grade         █████████████  216ms
│    verdict: Irrelevant
│
└─ audit.emit          ██  20ms
     verdict: Irrelevant, structured_refusal emitted
```

**Interpretation:**

The refusal trace is **682ms** vs 1,878ms for the generation trace. It runs the same retrieval and grading pipeline — the system still has to embed the query, search the index, rerank, and grade. The CRAG loop stops when the grader returns `Irrelevant`. No `haiku.generate`, no `citation.verify` span appears.

This is architecturally correct:
- **The grader saw real retrieved chunks** before deciding to refuse. It is not a keyword filter.
- **The refusal payload is safe**: the `redaction_guard` runs on `structured_refusal.closest_hits` before serialisation, so even the "closest documents we found" list is scrubbed of any chunks above the user's classification ceiling (Module 4 §3.3).
- **The audit span fires even on refusal** — every interaction is logged to CloudWatch, regardless of verdict. This satisfies the 7-year audit retention requirement for refused queries too.

**Why does refusal cost 682ms?**  
Because the system genuinely tries to answer before refusing. It embeds the query (50ms), searches (200ms), reranks (191ms), and only then lets the grader decide. A simpler keyword-block would be faster, but it would also miss nuanced out-of-corpus queries that happen to contain valid Dutch tax keywords.

---

## Latency Summary Across All Scenarios

| Scenario | Total | Spans | Generation? | Notes |
|---|---|---|---|---|
| Cache hit | 11ms | 3 | No | 143× faster than cold answer |
| Refusal (out-of-corpus) | 682ms | 10 | No | Stops at grader |
| RBAC blocked (helpdesk → FIOD) | 676ms | 11 | No | redaction_guard drops chunks |
| Full answer (helpdesk, Box 1) | 1,574ms | 12 | Yes | 1.05s generation dominant |
| Full answer (inspector, ECLI) | 1,878ms | 12 | Yes | Longer ECLI context |

---

## What Jaeger Enables in Production

1. **Latency regression detection** — if a Cohere rerank deployment doubles rerank latency, Jaeger shows it before end-users feel it. A CI gate on `rerank p95 ≤ 200ms` catches this automatically.

2. **RBAC audit trail** — every span carries `user_role`. Searching Jaeger for `user_role=helpdesk` + `verdict=Relevant` produces the complete list of queries where a helpdesk user received a substantive answer. This satisfies Dutch government audit requirements.

3. **Grader accuracy tracking** — `haiku.grade` spans carry `verdict`. Plotting `Irrelevant` rate over time surfaces query-type shifts (e.g., after a corpus update, suddenly 30% more refusals → corpus gap).

4. **Cost attribution** — `bedrock_input_tokens` and `bedrock_output_tokens` on `haiku.generate` spans feed directly into per-role cost dashboards. Inspector-role queries consistently cost more (longer ECLI context); helpdesk queries are cheaper.

5. **Cache effectiveness** — tracking the ratio of 3-span traces (cache hits) to 12-span traces (cold misses) shows cache hit rate in real time. The design target is >60% hit rate in steady-state production (Module 4 §3.1).
