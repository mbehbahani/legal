# Graph Report - Legal  (2026-05-28)

## Corpus Check
- 54 files · ~71,174 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1063 nodes · 1567 edges · 89 communities (71 shown, 18 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 209 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `05852a36`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]

## God Nodes (most connected - your core abstractions)
1. `UserContext` - 49 edges
2. `ChunkMeta` - 46 edges
3. `MockRAGClient` - 43 edges
4. `HaikuJudge` - 30 edges
5. `TelemetrySink` - 26 edges
6. `RAGResponse` - 25 edges
7. `UserContext` - 25 edges
8. `TelemetrySink` - 22 edges
9. `MockRAGClient` - 18 edges
10. `Graphify: Complete Student Guide` - 17 edges

## Surprising Connections (you probably didn't know these)
- `ChunkMeta` --shares_data_with--> `Module 1 — Ingestion & Knowledge Structuring`  [INFERRED]
  docs/ARCHITECTURE.md → design/module-1-2-retrieval.md
- `float` --uses--> `UserContext`  [INFERRED]
  tests/test_latency_budgets.py → tests/conftest.py
- `float` --uses--> `UserContext`  [INFERRED]
  tests/test_semantic_cache.py → tests/conftest.py
- `float` --uses--> `ChunkMeta`  [INFERRED]
  tests/seed_opensearch.py → tests/conftest.py
- `Process Report: How the Tax Authority RAG Architecture Was Built` --references--> `Master Plan — Tax Authority RAG Assignment`  [EXTRACTED]
  reports/PROCESS-REPORT.md → plans/MASTER-PLAN.md

## Communities (89 total, 18 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (35): AsyncOpenSearch, opensearch.sh script, OpenSearch, Redis, allowed_classifications(), async_opensearch_client(), bedrock_client(), bedrock_runtime() (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (28): ChunkMeta, HaikuJudge, _make_chunk(), MockRAGClient, int, RAGResponse, Thin wrapper around Bedrock Haiku 4.5 for LLM-as-judge calls.     temp=0, uses t, Deterministic stub simulating the CRAG pipeline output.     Used for tests that (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (42): Output, Scope, What to check, 6. Appendices, A. Cache Key Pseudo-Code (Full), B. RBAC Pre-Filter Helper (Python), C. Promotion Threshold Quick-Reference, code:python (CLASSIFICATION_ORDINAL = {"public": 0, "internal": 1, "fiod") (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (33): build_cache_key(), Canonical cache key construction (module-4 §2.2 + Appendix A).     Role-bound: d, Same query embedding bucket, same tax year, different roles →         different, Inspector and helpdesk keys differ even for identical queries., Full integration test: FIOD answer stored in Redis → helpdesk key lookup, _cosine(), float, test_semantic_cache.py — Semantic cache safety guarantees.  Threat/quality dimen (+25 more)

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (7): Docker Compose Stack, OpenSearch efficient_filter, Jaeger Tracing, Amazon OpenSearch Service, Role-Based Access Control (RBAC), Redis Stack, UserContext

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (15): extract_citation_tuples(), str, Step 1 + Step 2 of citation verifier (module-3 §4.1).     Returns (all_citations, Validates that the citation parser enforces lid + onderdeel depth,     not just, Parser extracts article, lid, onderdeel, and sub from a citation string., Parser extracts sub-level (e.g. sub 3) from a citation string., A citation citing lid 3 when only lid 2 is retrieved must be flagged         as, Citing onderdeel b when only onderdeel a is retrieved must fail.         Leden o (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (14): 4.5 Observability, Bedrock Cost Dashboard, code:mermaid (graph TD), Drift Alerts, Jaeger Deployment, OpenTelemetry Span Hierarchy, Span Attributes Inventory, 5.1 OpenTelemetry Span Hierarchy (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (31): answer_relevancy(), context_precision(), context_recall(), float, str, test_observability.py — OTel span emission + Ragas gates.  Threat/quality dimens, attempt_count and gen_retry_count must be observable per span., Simple precision-style metric: fraction of retrieved that are relevant. (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (31): bm25_rank(), dense_rank(), mock_rerank(), ndcg_at_k(), ChunkMeta, float, int, str (+23 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (13): 1.1 Chunking Strategy, 1.2 Hierarchical Metadata Schema, 1.3 Vector Database — Amazon OpenSearch Service, 1.4 Quantization & Memory Budget, Case Law (ECLI rulings), code:python (# LangChain-shaped — runnable shape, not full implementation), code:json (// Role: helpdesk — sees public only), Document-Level Security (DLS) — Backup Layer (+5 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (22): assert_no_fiod_content(), Assert that a response string contains no FIOD-classified content markers.     U, MockRAGClient, UserContext, Threat model: DIRECT TITLE ATTACK     A helpdesk user knows the exact title of a, Helpdesk queries exact FIOD memo title → must refuse with no FIOD content., Retrieved chunks for a helpdesk FIOD query must have zero FIOD-classified items., After a denied FIOD query, the telemetry sink must record a span         showing (+14 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (19): date, chunks_for_tax_year(), is_valid_on(), ChunkMeta, int, test_temporal_correctness.py — Temporal validity correctness.  Validates that th, Tests that the valid_from/valid_to date range filter excludes wrong versions., Chunk with valid_from=2024-01-01 is valid on 2024-06-01. (+11 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (20): build_structured_refusal(), ChunkMeta, HaikuJudge, str, test_rbac_redteam.py — Adversarial RBAC red-team test suite.  Every test in this, Threat model: EXISTENCE DISCLOSURE VIA STRUCTURED REFUSAL     Domain review find, All chunks (including FIOD) passed to _build_refusal; after redaction_guard,, After redaction_guard, public-classified chunks must still appear         in clo (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (26): Claude Haiku 4.5, RAG Evaluation Engineer — Test Suite Plan, 1. Deliverables (under `d:\AWS\Legal\tests\`), 2. Key Design Decisions, 3. Open Questions, 4. Dependencies, 5. Estimated Effort, RAG Evaluation Engineer — Test Suite Plan (+18 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (25): Deliverable format, Non-negotiables, Scope, Style, Jaeger, Module 4 Plan — Production Ops, Security & Evaluation, 1. Deliverables, 2. Key Design Decisions (+17 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (19): code:block1 (docker/), code:markdown (# Test Execution Results), Debugging tactics (use, don't skip), Deliverables, Non-negotiables, Results artifact (this is what the report-compiler reads), Scope, The loop (+11 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (23): 3.2 CRAG State Machine (LangGraph), code:mermaid (flowchart TD), 1. Architecture and design, 2. Evaluation harness, 3. Infrastructure scaffolding, 4. Reports and validation artifacts, Citation / attribution, code:mermaid (flowchart LR) (+15 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (14): MockRAGClient, UserContext, Tests that retrieval respects valid_from/valid_to date boundaries., Explicitly tests the year-confusion failure mode described in module-4 §2.3:, Near-miss test from module-4 §2.3 worked example:         'Box 1 rate 2023' vs ', 2022 Box 1 tarief query returns 2022 version (37,07% — same as 2024 but confirme, Domain review Check 4 (module-1-2-retrieval.md):     'The generation prompt shou, The 2020 version of art. 3.114 should be marked as superseded by the 2021 versio (+6 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (13): 3.6 Citation Verification Node, code:python (# Full depth: doc_id + article + lid + onderdeel + sub), code:block15 (chunk.doc_id == doc_id), code:python (def verify_citations(state: CRAGState) -> CRAGState:), code:python (span.set_attribute("citation.claims_count",      len(claims)), code:block19 (Citation Accuracy = (claims_count - unsupported_count) / cla), Fail-Closed Behavior, Module 4 Interface (+5 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (17): _percentile(), float, test_latency_budgets.py — TTFT and end-to-end latency SLAs.  Threat/quality dime, End-to-end p95 must be ≤ 4 seconds., Retrieval-stage p95 must be ≤ 300 ms (Module 4 promotion gate)., Constant must be aligned with module-4 §4.2 (200 ms cap)., Defensive: prevent silent drift of the SLA constants in conftest., Warm cache must never be slower than cold by more than measurement noise. (+9 more)

### Community 20 - "Community 20"
Cohesion: 0.21
Nodes (14): chunk_to_doc(), ensure_index(), generate_synthetic_fixtures(), main(), ChunkMeta, float, int, random_vector() (+6 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (15): test_ambiguity_refusal.py — CRAG fallback / refusal validation.  Threat/quality, structured_refusal payload must contain the contract fields., If response has no chunks, it must have no citations., Grader verdict must always be one of the documented enum values., attempt_count must never exceed the documented hard cap (= 2)., Out-of-corpus query must refuse with no citations and no answer., Under-specified query must not produce confident citations., Contradictory queries must not be 'confirmed' — fail-closed. (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.10
Nodes (28): Deliverable format, Non-negotiables, Scope, Style, Amazon OpenSearch Service, AWS Bedrock, Cohere embed-multilingual-v3, Master Plan — Tax Authority RAG Assignment (+20 more)

### Community 23 - "Community 23"
Cohesion: 0.36
Nodes (8): Appendix A — Configuration Cheat Sheet, Appendix B — Risk Register, code:mermaid (flowchart TD), Enterprise RAG Architecture for the National Tax Authority, Executive Summary, Requirements Traceability Checklist, System Overview Diagram, Enterprise RAG Architecture for the National Tax Authority

### Community 24 - "Community 24"
Cohesion: 0.17
Nodes (15): Claude Haiku 4.5, Corrective RAG (CRAG), 3.1 Model Configuration, 3. Retrieval Grader, 5. Loop Guard, 6. LangGraph Pseudo-code, 7. Per-Node Latency Budget, 8. Audit-Event Emission (Module 4 Observability) (+7 more)

### Community 25 - "Community 25"
Cohesion: 0.20
Nodes (10): 2.2 Node-by-Node Specification, code:json ({), `decide`, `generate`, `generate_with_disclosure`, `grade_documents`, `retrieve`, `structured_refusal` (+2 more)

### Community 26 - "Community 26"
Cohesion: 0.20
Nodes (11): 3.4 Retrieval Grader, code:python (GRADER_CONFIG = {), code:block11 (You are a retrieval-quality evaluator for a Dutch tax-law RA), code:block12 (## Sub-question), code:json ({), Model Configuration, Verbatim Grader Prompt Template, 3.2 Verbatim Grader Prompt Template (+3 more)

### Community 27 - "Community 27"
Cohesion: 0.24
Nodes (10): Architecture, Cache invariants, Cross-cutting facts (from the graph), Diagrams, God nodes (most-connected abstractions), Load-bearing security decision, Module 1 + 2 — Ingestion & Retrieval — [design/module-1-2-retrieval.md](../design/module-1-2-retrieval.md), Module 3 — Agentic RAG — [design/module-3-agentic.md](../design/module-3-agentic.md) (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.29
Nodes (10): Changing code — the loop, code:bash (# Find files / symbols connected to a concept), code:bash (# 1. Bring up dependencies), code:bash (pytest tests/test_rbac_redteam.py -v), Development Workflow, God nodes — handle with care, Prerequisites, Repo-understanding workflow (graphify) (+2 more)

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (9): Cache Poisoning / Tax-Year Ambiguity (Check 8), Citation Format (Check 1), Domain Review Findings, FIOD Classification (Check 5), Hierarchy Depth (Check 2), Legal Counsel Role (Check 7), Multilinguality (Check 6), Superseded / Consolidated Versions (Check 4) (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.16
Nodes (14): HaikuJudge, MockRAGClient, UserContext, test_citation_accuracy.py — Zero-hallucination citation guard.  Threat/quality d, When grounding is empty (CRAG Irrelevant path), the answer must contain     NO c, Query with no corpus match → refusal response must contain zero citation anchors, Ambiguous query with no corpus match must not contain a fabricated article numbe, test_faithful_claim_is_entailed() (+6 more)

### Community 31 - "Community 31"
Cohesion: 0.06
Nodes (37): ChunkMeta, Cohere embed-multilingual-v3, Cohere rerank-v3-5, 1.1 Chunking Strategy, 1.2 Hierarchical Metadata Schema, 1.3 Vector Database — Amazon OpenSearch Service, 1.4 Quantization & Memory Budget, 2.1 Hybrid Search Design (+29 more)

### Community 32 - "Community 32"
Cohesion: 0.22
Nodes (8): Cross-community bridges (high betweenness), Domain-review findings (from the design phase), Graph-derived risks, Inferred-edge confidence, Isolated nodes, Process / collaboration TODOs, Repository maturity caveats (from README), Risks & TODOs

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (7): code:block1 (tests/), Deliverables, Output, Scope, Stack constraints, Style, Test categories — be creative within each

### Community 34 - "Community 34"
Cohesion: 0.22
Nodes (9): 3.1 Query Transformation Layer — Routing Rule, code:block7 (Root question), Worked Example — Decomposition Tree, 1.1 Routing Rule, 1.2 Worked Example — Decomposition Tree, 1.3 Transform Node Pseudo-code, 1. Query Transformation Layer, code:block1 (Root question) (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (8): TelemetrySink, str, Returns {"result": "entailed"|"not_entailed", "explanation": str}.         Used, Returns {"is_refusal": bool, "leaks_forbidden_content": bool, "explanation": str, Returns a faithfulness score 0.0–1.0.         Each claim in the answer is checke, In-memory span collector. Tests inject spans; assertions check required attribut, SpanRecord, TelemetrySink

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (13): 3.3 State Schema, 3.5 Fallback Policy Table, 3.7 LangGraph Pseudo-code, 3.8 Per-Node Latency Budget, code:python (from langgraph.graph import StateGraph, END), code:python (from __future__ import annotations), Module 3 — Agentic RAG & Self-Healing, 2.1 Graph Diagram (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.09
Nodes (21): After (Gemini enriched): same query, Before (AST only): `graphify query "authentication boundary enforcement"`, code:block1 (Start nodes found: "Guard drops FIOD chunk...", ".test_seman), code:block2 (Start nodes found: "3.3 Three Enforcement Layers (Defense in), code:block3 ("Process Report: How the Tax Authority RAG Architecture Was ), Design docs (biggest gain), Docs I wrote (newly indexed), Graphify: AST-Only vs Gemini API Enrichment (+13 more)

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (6): code:json ({), Current Assignment Context, Deployment Notes, IAM Least-Privilege Policy — Tax Authority RAG, IAM Policy JSON, Required Actions

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): 1. Deliverables (file-by-file), 2. Key infra decisions (leaning), 3. Open questions, 4. Dependencies, 5. Effort + likely failure modes, docker-runner — Planning Phase

### Community 40 - "Community 40"
Cohesion: 0.12
Nodes (17): 5. Core Commands, code:powershell (graphify update .), code:powershell (graphify query "How does RBAC pre-filtering work?"), code:powershell (graphify explain "MockRAGClient"), code:powershell (graphify affected "HaikuJudge" --depth 2), code:powershell (graphify path "semantic cache" "RBAC"), code:powershell ($env:GEMINI_API_KEY = "your-key-here"), code:powershell (graphify watch .) (+9 more)

### Community 41 - "Community 41"
Cohesion: 0.52
Nodes (6): Agent definitions, Design docs (the "what"), Infrastructure (the "how to run"), Module Map, Reports (the "did it work"), Tests (the "proof")

### Community 42 - "Community 42"
Cohesion: 0.40
Nodes (5): main(), parse_junit(), int, str, Parse JUnit XML into per-suite pass/fail/skip counts.

### Community 43 - "Community 43"
Cohesion: 0.40
Nodes (4): Deliverable format, Non-negotiables, Scope, Style

### Community 44 - "Community 44"
Cohesion: 0.40
Nodes (4): code:block1 (# Enterprise RAG Architecture for the National Tax Authority), Inputs, Output, Tasks

### Community 45 - "Community 45"
Cohesion: 0.40
Nodes (5): Debugging History (Iterations to Green), Parameter Recommendations from Empirical Run, Runner Recommendations, Test Suite Summary, Validation — Test Plan & Execution Results

### Community 46 - "Community 46"
Cohesion: 0.20
Nodes (11): 4.3 RBAC — Three Enforcement Layers, code:python (def redaction_guard(chunks: list[Chunk], user: User) -> list), code:json ({), code:json ({), code:json ({), Layer 1 — OpenSearch `efficient_filter` + DLS (Primary), Layer 2 — Context-Level Redaction Guard (Secondary), Layer 3 — Immutable Audit Log (Tertiary) (+3 more)

### Community 47 - "Community 47"
Cohesion: 0.22
Nodes (9): 2.1 Hybrid Search Design, 2.2 Embeddings, 2.3 Reranker, 2.4 Parent-Document Retrieval at Generation Time, 2.5 Latency Budget, code:json ({), code:block6 ({), Hybrid + Filtered k-NN Query DSL (+1 more)

### Community 48 - "Community 48"
Cohesion: 0.60
Nodes (5): Audience for this overview, Core technology choices, Project Overview, What's in the repo (top-level), What this is

### Community 49 - "Community 49"
Cohesion: 0.40
Nodes (4): code:block1 (You are continuing work on the Tax Authority RAG architectur), Launch Prompt — Paste this into a fresh Claude Code session, What you'll get, Why a fresh session

### Community 50 - "Community 50"
Cohesion: 0.25
Nodes (8): code:block16 (System: You are a legal-text entailment checker.), Step 3 — NLI Grounding Judge (Haiku), 4.1 Algorithm, 4.2 Fail-Closed Behavior, 4. Citation Verification Node, code:block10 (ANCHOR_PATTERN = r'\(doc_id=(?P<doc_id>[^,]+),\s*art\.?\s*(?), code:block11 (System: You are a legal-text entailment checker.), code:python (def verify_citations(state: CRAGState) -> CRAGState:)

### Community 51 - "Community 51"
Cohesion: 0.50
Nodes (3): enabledMcpjsonServers, hooks, PreToolUse

### Community 52 - "Community 52"
Cohesion: 0.50
Nodes (3): graphify, graphify, Repository understanding rule

### Community 61 - "Community 61"
Cohesion: 0.17
Nodes (11): 12. The Benefit — Concrete Numbers, 13. Full Q&A Reference, code:powershell (graphify affected "HaikuJudge" --depth 2), code:javascript (const canvas = document.querySelector('canvas');), code:block37 (SETUP (once per repo)), From Zero to Knowledge Graph — Everything You Need to Know, Graphify: Complete Student Guide, Quick Reference Card (+3 more)

### Community 74 - "Community 74"
Cohesion: 0.18
Nodes (11): 11. Day-to-Day Workflow, After changing code, Before changing code, Before starting any task, code:powershell (# 1. Check if graph is stale), code:powershell (# Find the blast radius FIRST), code:powershell (graphify update .   # refresh graph, free, no API call), code:powershell ($env:GEMINI_API_KEY = "your-key") (+3 more)

### Community 75 - "Community 75"
Cohesion: 0.20
Nodes (10): 3. Installation, code:block10 ([graphify watch] Rebuilt: 865 nodes, 1188 edges, 80 communit), code:powershell (# IMPORTANT: Use python -m pip, not just pip), code:powershell (python -m pip show graphifyy    # confirm version), code:powershell (# Run from inside your repository folder), code:powershell (# AST-only extraction — FREE, no API key needed, ~2-5 second), Step 1 — Install the Python package, Step 2 — Verify installation (+2 more)

### Community 76 - "Community 76"
Cohesion: 0.20
Nodes (10): 9. Common Errors and Fixes, code:powershell (graphify explain "UserContext"), code:powershell (graphify query "UserContext callers dependencies"), code:powershell (graphify affected "tests_conftest_usercontext" --depth 2), code:powershell (# Always use python -m pip, not pip), Error: `graphify query` returns irrelevant nodes, Error: `ModuleNotFoundError: No module named 'graphify'` after install, Error: `No unique node match for UserContext` (+2 more)

### Community 77 - "Community 77"
Cohesion: 0.22
Nodes (10): 3.1 Pipeline Diagram with RBAC Pre-Filter Stage Highlighted, 3.2 Mathematical Proof: Why Post-Filtering Leaks, 3.3 Three Enforcement Layers (Defense in Depth), 3.4 OpenSearch DSL — Filtered k-NN Query, 3.5 Role Matrix, 3. RBAC — The Load-Bearing Section, code:mermaid (flowchart TD), code:python (def redaction_guard(chunks: list[Chunk], user: User) -> list) (+2 more)

### Community 78 - "Community 78"
Cohesion: 0.22
Nodes (9): Cache Poisoning / Tax-Year Ambiguity (Check 8), Citation Format (Check 1), Domain Review Findings, FIOD Classification (Check 5), Hierarchy Depth (Check 2), Legal Counsel Role (Check 7), Multilinguality (Check 6), Superseded / Consolidated Versions (Check 4) (+1 more)

### Community 79 - "Community 79"
Cohesion: 0.25
Nodes (8): 2. What Graphify is NOT, code:block3 (graphify dependencies:), code:block4 (You ask: "authentication boundary enforcement"), code:block5 (graphify = AST parser + graph construction + fuzzy text matc), NOT a question-answering system, NOT an NLP tool, NOT aware of meaning (without API key), What graphify IS (accurately)

### Community 80 - "Community 80"
Cohesion: 0.40
Nodes (5): 4.4 CI/CD Evaluation Gates, code:yaml (name: RAG Evaluation Gate), GitHub Actions CI Gate, Golden Test Set — 500 Q&A Pairs, Promotion Gate Thresholds

### Community 81 - "Community 81"
Cohesion: 0.20
Nodes (9): 4.1 Threat Model, 4.2 Semantic Cache, Cache Key Construction — Role-Bound, Year-Scoped, code:python (import hashlib, json), Cosine Threshold — 0.97 Floor, 0.98 Operational Default, Module 4 — Production Ops, Security & Evaluation, TTL Strategy, 2.4 TTL Strategy Tied to Legislative Effective Dates (+1 more)

### Community 82 - "Community 82"
Cohesion: 0.29
Nodes (7): 4.1 Golden Test Set — 500 Q&A Pairs, 4.2 Promotion Gate Thresholds, 4.3 Frameworks, 4.4 GitHub Actions CI Gate, 4.5 Shadow Deployment / Champion-Challenger, 4. CI/CD Evaluation Gates, code:yaml (name: RAG Evaluation Gate)

### Community 83 - "Community 83"
Cohesion: 0.29
Nodes (7): 4. The Three Integrations Graphify Installs, code:json ({), code:block12 ([graphify] Branch switched - launching background rebuild), Integration 1 — Claude Code hook (installed by `graphify claude install`), Integration 2 — Git hooks (installed by `graphify hook install`), Integration 3 — CLAUDE.md rules (installed by `graphify claude install`), Summary table

### Community 84 - "Community 84"
Cohesion: 0.29
Nodes (7): 6. Understanding the Outputs, code:gitignore (# Add to .gitignore), `graphify-out/graph.html`, `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`, `graphify-out/.graphify_analysis.json`, What to commit vs ignore

### Community 85 - "Community 85"
Cohesion: 0.29
Nodes (7): 7. AST-Only vs Gemini API Extraction, Query result comparison, Real numbers from this session, What API extraction adds ($0.06 for 49 files), What AST extraction does (free), When to re-run API extraction, Which backend to use

### Community 86 - "Community 86"
Cohesion: 0.33
Nodes (6): 10. Saving the Graph as an Image, code:javascript (const canvas = document.querySelector('canvas');), code:block29 (TypeError: Failed to execute 'serializeToString' on 'XMLSeri), Higher resolution export, Save as PNG (works, confirmed), Why SVG export fails

### Community 87 - "Community 87"
Cohesion: 0.28
Nodes (8): 1. Executive Summary & Threat Model, 2.1 Stack Choice: Redis Stack 7.4, 2.2 WARNING — The Cache Must Not Be Role-Blind, 2.3 Cosine Threshold — Why 0.97 Is the Floor, 2. Semantic Cache, code:python (import hashlib, json), Module 4 — Production Ops, Security & Evaluation, Module 4 — Production Ops, Security & Evaluation

### Community 88 - "Community 88"
Cohesion: 0.40
Nodes (5): 8. Can Claude CLI Replace the API Key?, code:block22 (Terminal only (no API, no Claude):), code:block23 ("redaction_guard()" --implements--> "access control enforcem), Summary, The one thing Claude cannot do that API extraction can

### Community 89 - "Community 89"
Cohesion: 0.50
Nodes (4): 1. What is Graphify?, code:block1 (Your repo files  →  graphify  →  graph.json + graph.html + G), code:powershell (python -m pip install graphifyy   # note: two y's — graphify), Install

## Knowledge Gaps
- **311 isolated node(s):** `npm`, `enabledMcpjsonServers`, `PreToolUse`, `app.sh script`, `jaeger.sh script` (+306 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Enterprise RAG Architecture for the National Tax Authority` connect `Community 23` to `Community 36`, `Community 9`, `Community 45`, `Community 47`, `Community 81`, `Community 87`, `Community 24`, `Community 31`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Module 4 — Production Ops, Security & Evaluation` connect `Community 87` to `Community 2`, `Community 4`, `Community 6`, `Community 77`, `Community 78`, `Community 82`, `Community 23`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `UserContext` connect `Community 1` to `Community 0`, `Community 35`, `Community 3`, `Community 5`, `Community 7`, `Community 8`, `Community 10`, `Community 11`, `Community 12`, `Community 17`, `Community 19`, `Community 30`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `UserContext` (e.g. with `str` and `ChunkMeta`) actually correct?**
  _`UserContext` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `ChunkMeta` (e.g. with `int` and `float`) actually correct?**
  _`ChunkMeta` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `MockRAGClient` (e.g. with `str` and `ChunkMeta`) actually correct?**
  _`MockRAGClient` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `HaikuJudge` (e.g. with `str` and `ChunkMeta`) actually correct?**
  _`HaikuJudge` has 23 INFERRED edges - model-reasoned connections that need verification._