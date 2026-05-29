# Knowledge Graph Build — Session Report
**Project:** Tax Authority Enterprise RAG  
**Date:** 2026-05-28  
**Main model:** claude-sonnet-4-6  
**Skill:** `/understand`

---

## What Is `/understand`?

The `/understand` skill analyzes a codebase and produces a `knowledge-graph.json` file — a structured representation of every file, class, function, concept, and their relationships. It powers an interactive dashboard for exploring project architecture without reading every file manually.

The skill runs as a **multi-phase orchestrator**: the main Claude session acts as a conductor, spawning specialized subagents for each phase, collecting their results, and assembling the final graph.

---

## Project Statistics

| Metric | Value |
|---|---|
| Files scanned | 65 |
| Languages detected | 11 (Python, Markdown, YAML, Shell, Dockerfile, JSON, JSONL, XML, INI, text) |
| Frameworks detected | pytest, Docker, OpenSearch, Redis Stack, AWS Bedrock, OpenTelemetry, Ragas, DeepEval |
| Total nodes in graph | 174 |
| Total edges in graph | 337 |
| Architectural layers | 9 |
| Guided tour steps | 10 |
| Subagents spawned | ~16 |
| Total session duration | ~20 minutes |

---

## Phase-by-Phase Breakdown

### Phase 0 — Pre-flight
No subagent. Performed inline:
- Verified git state (commit `02ea8ca`)
- Located the plugin at `~/.understand-anything-plugin`
- Created `.understand-anything/intermediate/` and `tmp/` directories
- Confirmed the `@understand-anything/core` package was already built

### Phase 0.5 — Ignore Configuration
No subagent. Ran a Node.js one-liner that read `.gitignore` and generated `.understand-anything/.understandignore` with suggested exclusion patterns. All patterns were left commented — the full codebase (including tests and scripts) was included in the analysis.

---

### Phase 1 — File Scan
**1 subagent** | Type: `Explore` (read-only)

Walked the entire directory tree, respecting built-in ignore patterns. For each file: detected language, counted lines, assigned a `fileCategory` (code / config / docs / infra / data / script), and resolved project-internal imports into an `importMap`.

**Output:** `scan-result.json` — 65 files catalogued across 11 languages.

---

### Phase 1.5 — Batch Computation
No subagent. Ran `compute-batches.mjs` locally — a Node.js script that uses the **Louvain community detection algorithm** on the import graph to group files into semantically related clusters. Produced **12 batches** (max 11 files, min 3 files per batch).

---

### Phase 2 — File Analysis
**12 subagents** | Type: `general-purpose` | Run up to 5 concurrently

The most expensive phase. Each subagent received a batch of files, read them carefully, and extracted:
- **File-level nodes** — one per file, with summary, tags, complexity
- **Child nodes** — classes, functions, concepts for important constructs
- **Edges** — imports, calls, depends_on, contains, documents, etc.

Batches were dispatched in three parallel waves:

| Wave | Batches | Files covered |
|---|---|---|
| Wave 1 | 1–5 | Python tests (11 files), Docker infra, agent definitions, root configs, architecture docs |
| Wave 2 | 6–10 | Docker env/IAM, healthcheck scripts, plan docs, reports, Jaeger trace JSONs |
| Wave 3 | 11–12 | Shell evaluation scripts, settings/golden QA data |

**Notable agents:**
- **Batch 1** (11 Python files, 1,207-line `conftest.py`) — largest batch; produced 64 nodes and 97 edges, took ~4 minutes
- **Batch 5** (4 architecture markdown docs, 3,084 lines total) — richest output; produced 46 nodes, 120 edges, and 33 concept nodes covering CRAG, RBAC, HNSW, hybrid retrieval, observability

**Problem encountered:** Most agents were denied the `Write` tool due to the project's permission settings. Agents returned their computed JSON as text in their result message, and the main session wrote the batch files manually. This is a known limitation of the permission model — the agents did the analysis correctly; only the write step needed a workaround.

**Schema normalization required:** Batch-5 used `from`/`to` instead of `source`/`target` for edges, and `description` instead of `summary` for nodes. Batch-8 used `relation` instead of `type`. A Python normalization pass fixed all inconsistencies before merging.

**Merge result:** 174 nodes, 337 edges. 4 duplicate nodes removed, 73 complexity fields defaulted to "moderate".

---

### Phase 3 — Graph Review
**1 subagent** | Type: `Explore` (read-only)

Read the assembled graph and produced a quality report. Findings:
- No dangling edges (all source/target nodes exist) ✓
- All files from the import map present in the graph ✓
- 61 nodes with missing `summary` fields (later auto-fixed)
- 1 orphan node (`config:.gitignore` — no edges)
- 304 edges missing unique `id` fields (cosmetic, not structural)

---

### Phase 4 — Architectural Layers
**1 subagent** | Type: `general-purpose`

Analyzed the file-node list and edge topology, then assigned every file-level node to one of 9 architectural layers:

| Layer | Node Count | What it covers |
|---|---|---|
| `layer:evaluation-harness` | 13 | `tests/` — test files, fixtures, golden QA, pytest config |
| `layer:architecture-design` | 9 | `design/` — module docs, FINAL doc, pipelines, schemas |
| `layer:infrastructure` | 13 | `docker/` — Compose, Dockerfile, env, healthchecks, requirements |
| `layer:runtime-services` | 7 | Virtual service nodes: OpenSearch, Redis, Jaeger, Bedrock, app |
| `layer:agent-orchestration` | 8 | `.claude/agents/` — all 8 Claude agent definition files |
| `layer:scripts-automation` | 5 | `scripts/` — shell + Python automation |
| `layer:planning-docs` | 6 | `plans/` — MASTER-PLAN and 5 agent sub-plans |
| `layer:reports-artifacts` | 9 | `reports/` — reports, trace JSONs, junit.xml |
| `layer:project-root` | 8 | README, assignment, root configs, MCP settings |

---

### Phase 5 — Guided Tour
**1 subagent** | Type: `general-purpose`

Designed a 10-step learning path through the codebase:

| Step | Title |
|---|---|
| 1 | Project Overview & Assignment |
| 2 | Multi-Agent Planning |
| 3 | Architecture Design Documents |
| 4 | Core Evaluation Harness |
| 5 | Docker Infrastructure |
| 6 | RBAC Red-Team & Security |
| 7 | CRAG & Citation Accuracy |
| 8 | Hybrid Retrieval & Temporal Correctness |
| 9 | Observability & Latency |
| 10 | Reports & Evaluation Results |

---

### Phase 6 — Validation
No subagent. An inline Node.js script validated the assembled graph:
- **First run:** 51 issues (all missing `summary`/`name` fields from batch-5 schema inconsistency)
- **Auto-fix:** Python normalization pass mapped `description` → `summary`, `label` → `name`, added default summaries where missing
- **Second run:** 0 issues ✓
- 5 pipeline/schema nodes were missing from layers → assigned to `layer:architecture-design`

### Phase 7 — Save
No subagent. Wrote `knowledge-graph.json`, built the structural fingerprints baseline (enables fast incremental updates on future runs), wrote `meta.json`, cleaned up all intermediate files.

---

## Model Usage

All agents in this session ran on **claude-sonnet-4-6**. No model overrides were set.

### Model Comparison for `/understand`

| Model | Speed | Cost | Quality | Best for |
|---|---|---|---|---|
| **claude-haiku-4-5** | Very fast | Cheapest | Shallow summaries, misses architectural concepts | Not recommended for /understand |
| **claude-sonnet-4-6** ✓ | Fast | Mid | Good — understood CRAG/RBAC/RAG concepts correctly | Projects up to ~200 files, well-documented codebases |
| **claude-opus-4-7** | Slower | 5–10× more | Deepest reasoning, most consistent schema adherence | Very large or complex codebases (500+ files, heavy abstraction) |

**Verdict for this project:** Sonnet was the right choice. The 65-file, well-documented codebase was within Sonnet's strengths. The schema inconsistencies (from/to vs source/target) that required normalization passes would be less frequent with Opus — it follows output schemas more precisely — but Sonnet produced correct analysis with minor post-processing.

---

## How to Relaunch the Dashboard

A launcher script is saved at `D:/AWS/Legal/launch-dashboard.ps1`.

**To use it:**
1. Open PowerShell
2. Run: `D:\AWS\Legal\launch-dashboard.ps1`
3. Look for the line: `🔑  Dashboard URL: http://127.0.0.1:5173/?token=XXXXXXXX`
4. Open that URL in your browser (the token changes each launch)
5. Keep the PowerShell window open while using the dashboard

---

## Potential Next Steps

### 1. Run `/understand --review` for deeper validation
The default validation is deterministic (structural checks only). Adding `--review` runs a full LLM-powered graph reviewer that checks semantic quality — whether summaries are accurate, whether important relationships were missed, whether concept nodes correctly represent the architecture.

```
/understand --review
```

### 2. Incremental updates after code changes
The fingerprints baseline is now saved. Next time you run `/understand` after making changes, it will detect which files changed and only re-analyze those — much faster than a full rebuild. The skill handles this automatically.

### 3. Run `/understand-chat` to query the graph
Once the graph exists, you can ask natural language questions about the codebase:
```
/understand-chat
```
Example questions:
- "Which files are responsible for RBAC enforcement?"
- "What does conftest.py export and who depends on it?"
- "Walk me through the CRAG loop from query to response."

### 4. Run `/understand-domain` for business domain extraction
Extracts the business domain knowledge embedded in the code — tax concepts, RBAC roles, document classifications, evaluation thresholds — and generates an interactive domain flow graph separate from the technical architecture graph.

### 5. Upgrade to Opus for a richer graph
If you want deeper summaries and more accurate concept extraction, re-run with Opus:
```
/understand --full
```
And change the model in Claude Code settings to `claude-opus-4-7` before running. This would particularly improve the concept nodes (currently 49 concepts — Opus would likely extract more nuanced relationships between them).

### 6. Add auto-update on commit
To have the graph automatically rebuild after each `git commit`:
```
/understand --auto-update
```
This writes `autoUpdate: true` to `.understand-anything/config.json`. The incremental update engine then re-analyzes only changed files on each commit.

### 7. Share with your team
The `knowledge-graph.json` file is self-contained. Anyone with the dashboard launcher can point it at the same file and explore the same graph. You could commit it to the repo (it's ~212 KB) so teammates get the graph without running the analysis themselves.

### 8. Generate an onboarding guide
```
/understand-onboard
```
Produces a structured onboarding document for new team members — explains the architecture, key files to read first, and common patterns — derived from the knowledge graph.

---

## Output Files

| File | Purpose |
|---|---|
| `.understand-anything/knowledge-graph.json` | The complete knowledge graph (212 KB) |
| `.understand-anything/meta.json` | Last analysis timestamp and commit hash |
| `.understand-anything/.understandignore` | File exclusion patterns |
| `launch-dashboard.ps1` | One-click dashboard launcher |
| `reports/understand-session-report.md` | This document |
