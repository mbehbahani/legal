# Master Plan — Tax Authority RAG Assignment

Synthesized from five sub-agent plans in `d:\AWS\Legal\plans\`, then revised to use **AWS Bedrock + Amazon OpenSearch + Jaeger** per user direction.

---

## A. Verified AWS access (us-east-1, account 780822965578)

| Service | Model / Resource | Status |
|---|---|---|
| LLM | `us.anthropic.claude-haiku-4-5-20251001-v1:0` (cross-region inference profile) | ✅ confirmed (PONG test) |
| Embeddings | `cohere.embed-multilingual-v3` | ✅ confirmed (1024-dim NL embedding) |
| Reranker | `cohere.rerank-v3-5:0` | ✅ confirmed (correctly ranked NL tax doc 0.88 vs off-topic 0.02) |
| Vector store | Amazon OpenSearch Service (managed) — to be provisioned | new |

⚠️ Currently authenticated as **root** (`arn:aws:iam::780822965578:root`). For production, switch to an IAM user/role scoped to `bedrock:InvokeModel` on the three model IDs above + OpenSearch domain access. Not a blocker for the assignment.

---

## B. What we'll deliver

```
d:\AWS\Legal\
├── design\
│   ├── module-1-2-retrieval.md        # ingestion, OpenSearch k-NN, hybrid, Cohere rerank
│   ├── module-3-agentic.md            # query transform, CRAG (Haiku grader), citation verifier
│   ├── module-4-ops-security.md       # cache, RBAC pre-filter, eval gates, Jaeger observability
│   └── FINAL-rag-architecture.md      # compiled submission-ready document
├── tests\                             # pytest + Ragas + DeepEval, Haiku as LLM-judge
├── docker\                            # Dockerfile + compose (opensearch, redis-stack, jaeger)
├── scripts\                           # run-eval, debug-shell, seed-corpus
└── reports\
    └── test-results.md                # captured by docker-runner, folded into FINAL
```

---

## C. Locked stack (revised)

| Decision | Pick | Why |
|---|---|---|
| **Vector store** | **Amazon OpenSearch Service** (Lucene engine, k-NN HNSW with `efficient_filter`) | Filter pushed *into* HNSW traversal → mathematically safe RBAC pre-filter; native BM25 in same engine eliminates separate sparse service; AWS-managed fits the AWS-only stack; Document-Level Security (DLS) as backup |
| **HNSW** | `m=32`, `ef_construction=256`, `ef_search=128` (tunable to 64 under load) | Recall ≥0.95 at 20M points |
| **Quantization** | OpenSearch FP16 scalar (2.13+); evaluate binary (2.16+) for memory at 20M scale | ~2× memory reduction with negligible recall loss; binary needs rescore step |
| **Embeddings** | **Cohere `embed-multilingual-v3` on Bedrock** (1024-dim) | NL-capable, EU-grade quality, AWS-resident; `input_type=search_document` for indexing, `search_query` for retrieval |
| **Chunking** | Structure-aware (Article/Paragraph/Sub) + parent-document retrieval; 256-token leaves, 1500-token parents | Cite granularity + LLM context |
| **Hybrid search** | OpenSearch native `hybrid` query (BM25 + k-NN) with RRF via search pipeline; regex router boosts BM25 on ECLI/article queries | Single engine, robust default, catches exact citations |
| **Reranker** | **Cohere `rerank-v3-5:0` on Bedrock** | Multilingual, AWS-resident (no egress), high quality (verified on Dutch query) |
| **Top-K cascade** | BM25 100 + k-NN 100 → RRF 60 → rerank top-8 | Fits 1.5s TTFT |
| **Generator + Grader + Judge LLM** | **Claude Haiku 4.5** via `us.anthropic.claude-haiku-4-5-20251001-v1:0` | One model for all, simplifies cost tracking + prompt management; cross-region inference profile is required (legacy on-demand IDs are deprecated) |
| **CRAG grader** | Haiku 4.5 with structured-output (tool-use JSON), `temp=0` | Multilingual, fast, deterministic |
| **Citation verifier** | Regex anchor check + Haiku NLI grounding judge, fail-closed | Zero-hallucination guarantee |
| **Loop guard** | Max 2 transform retries + 1 generation retry | Hard cap; protects TTFT |
| **Cache** | Redis Stack 7.4 (vector field) | One service for cache + session |
| **Cache cosine threshold** | 0.97 floor / 0.98 default | "Box 1 2023" vs "2024" embed at ~0.95 — anything lower yields wrong-year hits |
| **Cache key** | `SHA256(emb_bucket ‖ role ‖ classification_ceiling ‖ tax_year)` | Role-blind keys = side-channel; non-negotiable |
| **RBAC enforcement** | 3 layers: OpenSearch `efficient_filter` + DLS (primary), context redaction (secondary), audit log to CloudWatch + S3 with Object Lock (tertiary) | Pre-filter inside HNSW eliminates empty-set + timing leaks |
| **Eval frameworks** | Ragas (retrieval) + DeepEval (generation/red-team), Haiku as judge | Each tool used for its strongest metric |
| **Promotion gates** | Faithfulness ≥0.95, Ctx P/R ≥0.85/0.90, Citation Acc =1.00, p95 TTFT ≤1500ms, RBAC Leak =0 | RBAC leak is hard-fail |
| **Observability** | **OpenTelemetry → Jaeger** (all-in-one for dev; Cassandra/OpenSearch backend for prod). Optional Phoenix add-on for embedding drift dashboards. | OTLP-native, simpler ops than Langfuse |
| **Cost tracking** | Bedrock token counts emitted as Jaeger span attributes; CloudWatch dashboard aggregates per role/day | Visibility into Haiku + Cohere spend |
| **Test scope** | ~10 pytest files, 50-pair golden set, Haiku LLM-judge | Citation, RBAC, temporal, ambiguity, hybrid, cache, latency, observability |

---

## D. Docker stack (revised)

Local dev compose services:
- `app` — Python 3.12 slim, AWS SDK reads creds from env
- `opensearch` — single-node 2.18+ with security plugin enabled (DLS test)
- `redis-stack` — vector field for semantic cache
- `jaeger` — all-in-one (OTLP receiver on 4317, UI on 16686)
- ~~`ollama`~~ — **removed**, app calls Bedrock directly
- ~~`langfuse` + `postgres`~~ — **removed**, replaced by Jaeger

Required env vars (gitignored `.env`):
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
BEDROCK_LLM_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
BEDROCK_EMBED_ID=cohere.embed-multilingual-v3
BEDROCK_RERANK_ID=cohere.rerank-v3-5:0
OPENSEARCH_URL=https://opensearch:9200
OPENSEARCH_USER=admin
OPENSEARCH_PASS=...
REDIS_URL=redis://redis-stack:6379
OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4317
```

---

## E. Open questions — LOCKED (defaults accepted by user 2026-05-06)

| # | Question | Locked answer |
|---|---|---|
| 1 | OpenSearch deployment | **Managed Amazon OpenSearch Service**; t3.medium dev, m6g.large × 3 prod |
| 2 | Region | **us-east-1** (colocate with Bedrock) |
| 3 | Audit-log retention | **7 years** on S3 + Glacier transition after 1 yr |
| 4 | Web-search fallback | **No** — strict-corpus |
| 5 | Classification model | **Ordinal** (public < internal < fiod) |
| 6 | Cache invalidation on amendments | **Nightly diff** + manual flush hook |
| 7 | Corpus fixtures | **Synthesize ~250** spanning all doc_type/classification/tax-year combos |

**Scope: evidence-backed (all phases).**

---

## F. Execution sequence (locked: evidence-backed)

| Phase | Agents | Output | Wall-clock |
|---|---|---|---|
| 1. Design (parallel) | rag-retrieval-architect, agentic-rag-designer, mlops-security-architect | `design/module-1-2-retrieval.md`, `module-3-agentic.md`, `module-4-ops-security.md` | ~4–5h |
| 2. Domain review | legal-domain-reviewer | ⚠️/❌ findings appended in-place | 30–45 min |
| 3. Test design | rag-evaluation-engineer | `tests/` (~10 files + golden set + TEST-PLAN.md) | 3.5–4.5 d |
| 4. Build + run + debug | docker-runner | `docker/`, `scripts/`, `reports/test-results.md` | 1.5 d |
| 5. Technical compile | report-compiler | `design/FINAL-rag-architecture.md` (for reviewers of the *design*) | 1–2h |
| 6. Process / methodology report | **process-report-author** | `reports/PROCESS-REPORT.md` (for reviewers of the *agent architecture*) | 1–2h |

### Timing capture (for Phase 6)
The orchestrator must log every agent invocation to `reports/agent-timings.jsonl` as work progresses:
```json
{"agent":"rag-retrieval-architect","phase":1,"start":"2026-05-06T...","end":"...","duration_ms":...,"tokens_in":...,"tokens_out":...,"status":"completed"}
```
Without this data the process report cannot reconstruct the span empirically.

---

## G. Risks flagged

1. **OpenSearch security-plugin startup** in CI — first boot generates demo certs and can race; mitigated by `/_cluster/health?wait_for_status=yellow&timeout=60s` healthcheck.
2. **Bedrock throttling** during the eval run — Haiku has per-region TPM quotas; mitigate with adaptive retry + exponential backoff in the AWS SDK config; consider provisioned throughput if eval becomes regular.
3. **Cohere rerank latency** under load — Bedrock invocation adds network hop; budget 250ms p95, fall back to BM25-only if rerank times out.
4. **Cross-region inference profile** is required for Haiku 4.5; document this in the runbook so a future engineer doesn't try the on-demand model ID.
5. **Root credentials in use** — flagged above; create a least-privilege IAM user before any team-shared work.

---

## H. Status

- Defaults accepted for all 7 open questions ✓
- Scope: evidence-backed ✓
- AWS Bedrock access verified ✓
- Agent definitions written under `.claude/agents/` ✓
- New-session launch prompt: see `d:\AWS\Legal\NEXT-SESSION-PROMPT.md` ✓
- **Action**: close this Claude Code session, reopen, paste the launch prompt.
