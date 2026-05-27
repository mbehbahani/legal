# Graphify: AST-Only vs Gemini API Enrichment

**Date:** 2026-05-27
**Repo:** Tax Authority Enterprise RAG (d:\AWS\Legal)
**API used:** Gemini (Google AI Studio, free tier)
**Cost:** $0.06 (82,988 tokens in / 6,187 tokens out)

---

## What changed — numbers

| Metric | AST only (before) | Gemini enriched (after) | Change |
|---|---|---|---|
| Nodes | 865 | 885 | +20 |
| Edges | 1,188 | 1,248 | +60 |
| Communities | 80 | 73 | -7 (better clustering) |
| EXTRACTED edges | ~1,000 | ~1,054 | +54 semantic |
| INFERRED edges | 194 (avg conf. 0.52) | fewer | replaced by real extractions |
| Isolated nodes | 294 | fewer | semantic pass connected stragglers |

---

## Which files were affected

The Gemini pass re-extracted **56 files** across the whole repo. The most meaningful changes happened in these categories:

### Design docs (biggest gain)
| File | What changed |
|---|---|
| [design/module-4-ops-security.md](../design/module-4-ops-security.md) | Sections now have semantic `--contains-->` edges to their subsections. "3.3 Three Enforcement Layers" now explicitly links to Layer 1, Layer 2, Layer 3, the DSL query, and the Role Matrix. Before: only heading nodes existed, no structure between them. |
| [design/module-3-agentic.md](../design/module-3-agentic.md) | CRAG node states (`retrieve`, `grade_documents`, `decide`, `generate`, `transform_query`, `verify_citations`, `structured_refusal`) are now their own nodes in community 25 with edges between them. |
| [design/module-1-2-retrieval.md](../design/module-1-2-retrieval.md) | `ChunkMeta` now has an EXTRACTED `shares_data_with` edge to "Module 1 — Ingestion & Knowledge Structuring" (previously only INFERRED). |
| [design/FINAL-rag-architecture.md](../design/FINAL-rag-architecture.md) | Layer 1/2/3 RBAC nodes became first-class with `--contains-->` edges from "4.3 RBAC — Three Enforcement Layers". |

### Docs I wrote (newly indexed)
The five `docs/` files I created were treated as first-class content and got their own communities:

| File | Community (after) | Nodes extracted |
|---|---|---|
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | C27 | `God nodes`, `Cache invariants`, `Load-bearing security decision`, `The four modules`, `Cross-cutting facts` |
| [docs/DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) | C28 | `Repo understanding workflow`, `God nodes — handle with care`, `Changing code — the loop`, `Prerequisites` |
| [docs/TODO_RISKS.md](TODO_RISKS.md) | C32 | `Inferred-edge confidence`, `Isolated nodes`, `Cross-community bridges`, `Domain review findings` |
| [docs/MODULE_MAP.md](MODULE_MAP.md) | C41 | `Design docs — the what`, `Tests — the proof`, `Infrastructure`, `Reports`, `Agent definitions` |
| [docs/PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | C48 | `What this is`, `Core technology choices`, `What's in the repo` |

This means you can now `graphify query "god nodes blast radius"` and it will find [docs/DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) correctly, because the docs are part of the graph.

### New concept nodes (semantic-only, didn't exist in AST)
Gemini created dedicated concept nodes for technology terms that appeared across many files but weren't code symbols:

| New node | Connects to |
|---|---|
| `efficient_filter` | community 4 (RBAC design) |
| `rbac` | community 4 |
| `user_context` | communities 1, 4 |
| `chunk_meta` | communities 1, 30 |
| `redis_stack` | community 4 |
| `claude_haiku_4_5` | community 13 (test results) |
| `claude_haiku` | community 24 (CRAG design) |
| `crag` | community 24 |
| `aws_bedrock` | community 22 (plans) |
| `cohere_embed_multilingual_v3` | community 35 |
| `cohere_rerank_v3_5` | community 30 |
| `amazon_opensearch` | community 35 |
| `jaeger` | community 14 |

These nodes act as **cross-file bridges** — a query for "Cohere reranker" now traverses from the design doc section to the test that validates it.

---

## How the queries changed

### Before (AST only): `graphify query "authentication boundary enforcement"`

```
Start nodes found: "Guard drops FIOD chunk...", ".test_semantic_fiod_response_does_not_leak_existence()"
— matched test string fragments, not the architecture concept
Result: 36 nodes, mostly test class names and fixture references
Missing: redaction_guard(), efficient_filter sections, Layer 1/2/3 nodes
```

### After (Gemini enriched): same query

```
Start nodes found: "3.3 Three Enforcement Layers (Defense in Depth)", "4.3 RBAC — Three Enforcement Layers"
— matched the actual design sections semantically
Result: 30 nodes, directly the RBAC architecture
Includes: Layer 1 (efficient_filter + DLS), Layer 2 (redaction_guard), Layer 3 (audit log),
          OpenSearch DSL query node, Mathematical Proof node, Role Matrix
```

**Root cause of the improvement:** Gemini read the section heading "Three Enforcement Layers (Defense in Depth)" and understood it relates to "authentication boundary enforcement" as a concept, even though the words don't overlap. The new EXTRACTED edges (`4.3 RBAC --contains--> Layer 1`, etc.) gave the BFS traversal the right paths to follow.

---

## What the API enrichment physically did

### Step 1 — AST extraction (same as before, free)
Tree-sitter parsed all 21 code files → function definitions, class definitions, call edges, parameter types.

### Step 2 — Semantic extraction (new, costs tokens)
Gemini read 35 doc/markdown files in 2 chunks (token budget: 60,000 per chunk). For each chunk it:
- Identified section hierarchy → created `--contains-->` edges between headings and their content
- Recognized technology concepts → created concept nodes (`efficient_filter`, `crag`, etc.)
- Detected cross-file references → created `--references-->` and `--shares_data_with-->` edges

### Step 3 — Deduplication
57 nodes deduplicated: 27 exact matches (same label, different file), 29 fuzzy matches (e.g. "UserContext" appearing in conftest + test files → kept the conftest version as primary).

### Step 4 — Community re-clustering
Louvain algorithm re-ran with the new edges. Result: 80 → 73 communities. The 7 merged communities were thin clusters that the new edges connected to larger ones.

---

## New "surprising connection" discovered by Gemini

The analysis file flagged one new EXTRACTED surprising connection (the others were already known INFERRED ones):

```
"Process Report: How the Tax Authority RAG Architecture Was Built"
    --references-->
"Master Plan — Tax Authority RAG Assignment"

Source files: reports/PROCESS-REPORT.md → plans/MASTER-PLAN.md
Confidence: EXTRACTED (not guessed)
Why surprising: bridges separate communities (reports vs plans)
```

This connection was invisible in the AST graph because it's a prose reference in a markdown file — no import, no function call. Only the semantic pass found it.

---

## What did NOT change

- **God nodes are the same:** `UserContext` (49 edges), `ChunkMeta` (45), `MockRAGClient` (41), `HaikuJudge` (30), `RAGResponse` (25). Their edge counts are stable — these are structural facts from the code, not affected by semantic enrichment.
- **Test communities are the same:** communities 3, 5, 7, 8, 10, 11, 12, 17, 19, 21 (all test files) — AST extraction was already accurate for Python code.
- **graph.html re-rendered** with the enriched data. Open [graphify-out/graph.html](../graphify-out/graph.html) to see the denser semantic connections visually.
- **Future `graphify update .` is free** — the semantic annotations are now baked into graph.json. Incremental rebuilds only re-run the LLM on files that actually changed.

---

## When to re-run `graphify extract`

| Trigger | Action |
|---|---|
| Code change (function rename, new test) | `graphify update .` — free, AST-only |
| New design doc or significant prose change | `graphify extract . --backend gemini` — ~$0.01–0.05 depending on size |
| Added new docs/ files (like this one) | `graphify extract . --backend gemini` — it will only re-extract changed files |
| Architecture refactor affecting many files | `graphify extract . --backend gemini --force` |

The `--force` flag overwrites graph.json even if the rebuild has fewer nodes (useful after deleting files).

---

## Summary: is the API worth it?

| Scenario | AST only | With API |
|---|---|---|
| Finding a function, its callers, its tests | Excellent | Same |
| "What does X concept mean in this codebase?" | Poor (word matching only) | Good (semantic bridge) |
| Cross-vocabulary queries ("authentication" → "RBAC") | Fails | Works |
| Design doc ↔ code traceability | Weak | Strong |
| Onboarding a new contributor | Moderate | Strong |
| Cost | Free | $0.06 one-time, ~$0.01 incremental |

**Verdict:** For a repo like this — where design docs and code use different vocabularies for the same concepts — the $0.06 semantic extraction is high value. The graph is now permanently smarter for all future queries, by anyone, in any tool that reads graph.json.
