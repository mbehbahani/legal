# RAG Evaluation Engineer — Test Suite Plan

Scope: build a runnable, adversarial test suite for the Tax Authority RAG (500k docs, RBAC, zero-hallucination, <1.5s TTFT). Stack: pytest + Ragas + DeepEval, with LLM-as-judge for citation/faithfulness.

## 1. Deliverables (under `d:\AWS\Legal\tests\`)

1. `conftest.py` — shared fixtures: client, test users (helpdesk / inspector / legal / FIOD), corpus loader, LLM-judge client, Redis cache handle, telemetry sink.
2. `golden/golden_set.jsonl` — ~50 curated Q&A pairs; min 1 per doc_type (legislation, case law, policy, e-learning), with expected citations, classification, temporal tag, allowed roles.
3. `test_citation_accuracy.py` — Ragas Faithfulness + DeepEval `FaithfulnessMetric` + custom (claim, paragraph) LLM-judge verifying every claim maps to a returned chunk; fails on any uncited claim.
4. `test_rbac_redteam.py` — adversarial RBAC: direct title query, semantic-FIOD paraphrase, cache-poisoning replay across roles, prompt-injection ("ignore filters"), citation-leak via error messages, embedding-inversion stretch.
5. `test_temporal_correctness.py` — 2021/2023/2024 Box-1 rate queries; asserts retrieved law version matches query year; checks `valid_from`/`valid_to` metadata respected.
6. `test_ambiguity_refusal.py` — out-of-corpus, contradictory, under-specified queries; asserts CRAG grader routes to "Irrelevant/Ambiguous" and system refuses or asks clarifying question (no fabrication).
7. `test_hybrid_retrieval.py` — exact ECLI lookups (`ECLI:NL:HR:2023:123`) must hit BM25 top-1; semantic queries hit dense top-5; RRF fusion sanity; reranker improves nDCG@5.
8. `test_cache_safety.py` — semantic cache near-miss: "Box 1 2023" vs "Box 1 2024" must NOT collide at threshold; classification-aware cache key; per-role cache partitioning.
9. `test_latency_budgets.py` — pytest-benchmark: TTFT p95 <1.5s, end-to-end p95 <4s, retrieval <300ms, rerank <200ms; cold vs warm cache.
10. `test_observability.py` — every request emits trace_id, role, retrieval_scores, grader_verdict, citations; Ragas ContextPrecision/Recall + AnswerRelevancy thresholds enforced as gate.

## 2. Key Design Decisions

- **Framework split:** pytest runner; Ragas for ContextPrecision/Recall/Faithfulness/AnswerRelevancy; DeepEval for G-Eval custom rubrics + RBAC red-team patterns. One metric per strongest tool, no duplication.
- **Golden-set curation:** I curate ~50 pairs by hand — 8 temporal, 6 ECLI exact-match, 10 RBAC-sensitive, 8 ambiguous/refusal, rest general. JSONL for diffability and CI gating.
- **LLM-judge model:** **Claude Haiku 4.5 via Bedrock** (`us.anthropic.claude-haiku-4-5-20251001-v1:0`, temp=0, confirmed working). Same model used by the system itself, so judge stays consistent with grader behavior. Cost-effective for the 50-pair × N-claim evaluation matrix.
- **RBAC red-team breadth:** minimum 4 threat models — direct title, semantic-FIOD paraphrase, cache-poisoning cross-role, prompt-injection; plus citation-leak and embedding side-channel as stretch.
- **Latency enforcement:** pytest-benchmark for percentile reporting; custom asyncio harness for TTFT specifically (benchmark measures total). Both required.
- **Fixture corpus:** ~200 synthetic + 50 real anonymized docs spanning all doc_types, classifications, and 2019–2024 vintages. Big enough for meaningful retrieval, small enough for CI.
- **Mocking strategy:** prefer real services (Qdrant + Redis + reranker via docker-compose). Mock only the LLM generator behind a deterministic stub for non-judge tests; judge calls hit the real model.

## 3. Open Questions

- Existing golden set, or curate from scratch (default: curate ~50)?
- NL legal fixtures (Wet IB, ECLI samples) provided, or synthesize ~250?
- Bedrock spend ceiling for the eval run? (Estimate: ~$2–5 per full pass at Haiku rates.)
- CI environment AWS auth — env vars from secrets manager or assumed-role via OIDC?

## 4. Dependencies

Needs from design agents: metadata schema (ingestion), classification taxonomy (security), cache-key spec (ops), CRAG grader output schema (agentic), reranker contract (retrieval). Provides to docker-runner: pytest entrypoint, env-var contract, fixture seed scripts.

## 5. Estimated Effort

3.5–4.5 engineer-days: 0.5d golden set, 0.5d conftest/fixtures, 2d test files, 0.5d CI wiring + thresholds, 0.5d flake hardening.
