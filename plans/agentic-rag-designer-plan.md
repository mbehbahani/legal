# Module 3 (Agentic RAG & Self-Healing) — Designer Plan

## 1. Deliverables
- File: `d:\AWS\Legal\design\module-3-agentic.md`
- Section outline (1 line each):
  1. **Overview & design goals** — zero-hallucination, TTFT budget, regulated-domain constraints.
  2. **Query Transformation Layer** — router + decomposition + HyDE + step-back prompting.
  3. **CRAG State Machine (LangGraph)** — nodes, edges, conditional routing diagram.
  4. **Retrieval Grader** — model choice, prompt, structured output schema, calibration.
  5. **Fallback Policy per Verdict** — actions for Relevant / Ambiguous / Irrelevant.
  6. **Citation Verification Node** — grounding check, regex anchors, fail-closed behavior.
  7. **State Schema & Loop Guard** — typed state, retry counters, termination conditions.
  8. **Pseudo-code** — LangGraph node stubs + Pydantic schemas.
  9. **Interfaces** — inputs from Module 2 (retrieval), outputs to Module 4 (ops/eval).
  10. **Risks & Mitigations** — latency, prompt-injection, grader drift.

## 2. Key Design Decisions (current leaning)
1. **Query-transform routing rule** — small router LLM (Haiku-tier) classifies the query:
   - >1 distinct legal concept or conjunctions ("and/plus/also") → **Decompose** into sub-queries.
   - Vague/under-specified semantic query, no exact identifiers → **HyDE** (synthesize a hypothetical ruling/article paragraph, embed it).
   - Narrow factual lookup that fails initial retrieval → **Step-back** to a broader concept.
   - Exact ID (ECLI, article number) → skip transforms; straight to hybrid retrieval.
2. **Grader model** — **Claude Haiku 4.5 via Bedrock** (`us.anthropic.claude-haiku-4-5-20251001-v1:0`, cross-region inference profile, confirmed working) with structured-output JSON via tool-use, `temperature=0`, `max_tokens=200`. NOT a fine-tuned classifier. Faster iteration, multilingual (NL/EN), prompt-tunable for corpus drift. Fine-tuned classifier deferred to v2.
3. **Grader output schema** — per chunk: `{verdict: Relevant|Ambiguous|Irrelevant, confidence: 0–1, reason: str, missing_aspects: list[str]}`, plus aggregated doc-level verdict. Confidence enables threshold-tunable routing.
4. **Fallback policy**:
   - **Relevant** → generate, then citation-verifier gate.
   - **Ambiguous** → step-back rewrite + re-retrieve once; if still ambiguous, return clarifying question (no hallucination).
   - **Irrelevant** → decompose → re-retrieve; if still irrelevant and web-search allowed, scoped search of `.overheid.nl` / `rechtspraak.nl`; else return "no grounded answer found" with closest hits as suggestions.
5. **Citation verifier** — hybrid: (a) regex/anchor check that every cited `(doc_id, article, paragraph, sub)` exists in retrieved chunks, (b) NLI-style LLM grounding check per claim. Fail-closed: any unsupported claim → regenerate with stricter prompt or downgrade to "partial answer".
6. **Loop guard** — max 2 transform retries + 1 generation retry (hard cap = 3 LLM-generation cycles). Tracked in state; on exhaustion → structured "insufficient evidence" response.
7. **State schema fields** — `original_query, transformed_queries[], retrieval_strategy, chunks[], grades[], verdict, attempt_count, transform_history[], draft_answer, citation_check, final_answer, user_role` (RBAC propagation through every node).

## 3. Open Questions (user input would change design)
- Per-node latency budget within the 1.5s TTFT envelope? (Drives parallel-per-chunk vs. batched grading via Bedrock concurrency.)
- Web-search fallback (overheid.nl / rechtspraak.nl) permitted, or strict-corpus-only?
- Is "ask clarifying question" UX acceptable, or must the system always attempt an answer?
- Bedrock provisioned throughput planned for grader hot path, or rely on on-demand?

## 4. Dependencies
- **From Retrieval Architect (Module 2)**: chunk schema `{text, doc_id, doc_type, article, paragraph, sub, hierarchy_path, version_date, security_class}`; retrieval API `retrieve(query, role, top_k, strategy) → List[Chunk]`; rerank score field; confirmation that BM25 + dense fusion supports re-calls with rewritten queries.
- **To Ops/Security (Module 4)**: graded-verdict event schema for observability (per-query: verdicts, attempts, transform path, per-node latency); citation-verifier output `{claims[], grounded: bool, unsupported_claims[]}` feeding Faithfulness / Context-Precision in Ragas/DeepEval; RBAC role propagated through state for audit.

## 5. Estimated Effort
Full module write-up: **4–5 hours** — ~1.5h CRAG graph diagram + node specs, 1h grader prompt + schemas, 1h citation verifier logic + pseudo-code, 0.5h fallback decision table, 0.5–1h interfaces/risks polish.
