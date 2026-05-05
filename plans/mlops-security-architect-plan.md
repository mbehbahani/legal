# Module 4 Plan — Production Ops, Security & Evaluation

## 1. Deliverables
- **File:** `d:\AWS\Legal\design\module-4-ops-security.md`
- **Section outline (one line each):**
  1. Executive summary + threat model (helpdesk vs. inspector vs. FIOD analyst).
  2. Semantic Cache — Redis Stack, threshold, role-bound key, TTL tied to legislative validity.
  3. RBAC — index-level pre-filter (primary), context redaction guard (secondary), audit log (tertiary), with mathematical leak proof.
  4. CI/CD Evaluation Gates — Ragas (retrieval) + DeepEval (generation), 500-item golden set, promotion thresholds, GitHub Actions snippet, shadow / champion-challenger.
  5. Observability — OpenTelemetry → Langfuse + Phoenix, per-query metrics, drift alerts.
  6. Role matrix + appendix (pseudo-code, Mermaid diagrams, threshold table).

## 2. Key Design Decisions
1. **Cache backend:** Redis Stack (RediSearch + HNSW vector field). On-prem deployable, sub-ms KNN; GPTCache rejected (extra service, weaker auth model).
2. **Cosine threshold:** 0.97 floor / 0.98 default. "Box 1 rate 2024" vs "Box 1 rate 2023" embed at ~0.95 — anything below 0.97 yields financially wrong hits.
3. **Cache-key role binding:** `SHA256(query_embedding_bucket || user.role || user.classification_ceiling || tax_year_context)`. Role-blind keys = confused-deputy side channel. Non-negotiable.
4. **Three-layer RBAC:** (a) **OpenSearch `efficient_filter` (Lucene engine)** + Document-Level Security (DLS) — primary; (b) context redaction guard for mislabeled payloads — secondary; (c) immutable audit log `(user, query, doc_ids, citations)` to **CloudWatch + S3 with Object Lock** — tertiary.
5. **Pre-filter pipeline stage:** `efficient_filter` clause runs *inside* HNSW traversal (Lucene engine, OpenSearch ≥2.4). Math: post-filtering top-K leaks via (i) empty-set inference when FIOD docs dominate the neighborhood, (ii) timing side-channel from differential traversal cost. `efficient_filter` prunes candidates before scoring → eliminates both.
6. **Eval split:** Ragas → Faithfulness, Context Precision/Recall, Answer Relevancy. DeepEval → Citation-Accuracy custom assertion, hallucination, RBAC red-team, latency.
7. **Promotion gates:** Faithfulness ≥0.95, Ctx Precision ≥0.85, Ctx Recall ≥0.90, Answer Relevancy ≥0.90, Citation Accuracy =1.00, p95 TTFT ≤1500 ms, RBAC Leak Rate =0.00 (hard fail).
8. **Observability:** OTel SDK in LangGraph nodes → OTLP → **Jaeger** (trace UX, all-in-one for dev, scaled deployment with Cassandra/OpenSearch backend for prod) + optional Phoenix add-on for embedding-drift dashboards. Bedrock token counts emitted as span attributes for cost tracking; CloudWatch dashboard aggregates per-role/day.

## 3. Open Questions
- AWS region for OpenSearch + Bedrock: us-east-1 (current Bedrock home) or eu-central-1 (NL residency, needs Cohere availability check)?
- Audit-log retention: 1 / 3 / 7 yr (tax norms ≈7 yr)?
- Cache invalidation on amendments: law-change event bus or nightly effective-date diff?
- `classification` ordinal (PUBLIC<INTERNAL<FIOD) or compartments (Bell-LaPadula)? Changes filter predicate.
- Bedrock IAM: per-role IAM users for the app, or single service role with role-aware request signing?

## 4. Dependencies
- **Retrieval architect:** metadata schema — `classification`, `effective_date`, `tax_year`, `doc_type`; OpenSearch index mapping with `efficient_filter`-compatible `keyword` fields.
- **Agentic designer:** grader-verdict enum (Relevant/Ambiguous/Irrelevant) for dashboards + drift detection.
- **Domain reviewer:** sign-off on role matrix and threshold values.

## 5. Estimated Effort
Full module write-up: ~6–8 focused hours (≈1500–2000 lines markdown incl. Mermaid diagrams, pseudo-code, threshold table, CI YAML, role matrix).
