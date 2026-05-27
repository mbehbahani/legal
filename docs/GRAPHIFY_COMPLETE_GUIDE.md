# Graphify: Complete Student Guide
## From Zero to Knowledge Graph — Everything You Need to Know

**Based on:** A real working session on the Tax Authority Enterprise RAG repository
**Date:** 2026-05-27
**Repository:** d:\AWS\Legal (865–885 nodes, 1,188–1,248 edges, 49 files)

---

## Table of Contents

1. [What is Graphify?](#1-what-is-graphify)
2. [What Graphify is NOT](#2-what-graphify-is-not)
3. [Installation](#3-installation)
4. [The Three Integrations Graphify Installs](#4-the-three-integrations-graphify-installs)
5. [Core Commands](#5-core-commands)
6. [Understanding the Outputs](#6-understanding-the-outputs)
7. [AST-Only vs Gemini API Extraction](#7-ast-only-vs-gemini-api-extraction)
8. [Can Claude CLI Replace the API Key?](#8-can-claude-cli-replace-the-api-key)
9. [Common Errors and Fixes](#9-common-errors-and-fixes)
10. [Saving the Graph as an Image](#10-saving-the-graph-as-an-image)
11. [Day-to-Day Workflow](#11-day-to-day-workflow)
12. [The Benefit — Concrete Numbers](#12-the-benefit--concrete-numbers)
13. [Full Q&A Reference](#13-full-qa-reference)

---

## 1. What is Graphify?

Graphify is a **repository understanding tool**. It reads your codebase and documentation, converts everything into a knowledge graph (nodes = symbols/concepts, edges = relationships), and lets you query that graph in plain English instead of grepping through files.

```
Your repo files  →  graphify  →  graph.json + graph.html + GRAPH_REPORT.md
                                        ↓
                              graphify query "your question"
                                        ↓
                              Relevant subgraph (nodes + edges)
```

The graph answers questions like:
- "What calls `redaction_guard()`?"
- "What is the blast radius if I change `UserContext`?"
- "How are the cache key and RBAC connected?"
- "Where does authentication enforcement happen?"

### Install

```powershell
python -m pip install graphifyy   # note: two y's — graphifyy
```

It installs 28 packages including tree-sitter grammars for 25+ languages.

---

## 2. What Graphify is NOT

This is critical to understand before using it.

### NOT an NLP tool
```
graphify dependencies:
  tree-sitter       ← AST parser (code structure)
  networkx          ← graph algorithms
  datasketch        ← MinHash / probabilistic similarity
  rapidfuzz         ← fuzzy STRING matching
  numpy / scipy     ← math

No NLP libraries: no spaCy, no transformers, no NLTK, no embeddings
```

### NOT a question-answering system
When you run `graphify query "How does RBAC work?"`, graphify does NOT:
- Understand your question semantically
- Write a prose answer
- Reason about your code

What it DOES:
1. Fuzzy-matches your question words against node labels in the graph
2. Finds the closest matching start nodes
3. Runs BFS (breadth-first search) graph traversal from those nodes
4. Returns the subgraph of connected nodes and edges

**The prose answer you see is always YOU or your AI assistant synthesizing the returned nodes** — not graphify.

### NOT aware of meaning (without API key)
```
You ask: "authentication boundary enforcement"
Graphify looks for: nodes containing "authentication", "boundary", "enforcement"
Your code uses:     "RBAC", "efficient_filter", "classification_ceiling"

Without API key → vocabulary mismatch → poor results
With API key    → Gemini read your docs and bridged the gap → good results
```

### What graphify IS (accurately)
```
graphify = AST parser + graph construction + fuzzy text matching + graph traversal
         + optional LLM enrichment (via external API key)
```

Think of it as a **smart map of your repository**, not a smart assistant.

---

## 3. Installation

### Step 1 — Install the Python package

```powershell
# IMPORTANT: Use python -m pip, not just pip
# Your machine may have multiple Python versions with separate pip executables

python -m pip install graphifyy
```

**Why `python -m pip` instead of `pip`?**
On Windows with multiple Python versions, `pip` might point to a different Python than `python`. Using `python -m pip` guarantees they match.

### Step 2 — Verify installation

```powershell
python -m pip show graphifyy    # confirm version
graphify --help                 # confirm CLI is on PATH
```

### Step 3 — Install Claude Code integration

```powershell
# Run from inside your repository folder
graphify claude install
```

This does TWO things simultaneously (people confuse these):
1. Writes a `## graphify` section to `CLAUDE.md` — rules for how Claude should use the graph
2. Registers a `PreToolUse` hook in `.claude/settings.json` — makes Claude consult the graph automatically before answering codebase questions

### Step 4 — Build the initial graph

```powershell
# AST-only extraction — FREE, no API key needed, ~2-5 seconds
graphify update .
```

Output you'll see:
```
[graphify watch] Rebuilt: 865 nodes, 1188 edges, 80 communities
[graphify watch] graph.json, graph.html and GRAPH_REPORT.md updated in graphify-out
```

---

## 4. The Three Integrations Graphify Installs

Students often confuse these because they all sound similar. They are completely separate.

### Integration 1 — Claude Code hook (installed by `graphify claude install`)
**File:** `.claude/settings.json`
**What:** Tells Claude Code to consult the graph before answering architectural questions
**Trigger:** Every time Claude Code reads or runs a tool in this repo
```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash", "hooks": [...] }]
  }
}
```

### Integration 2 — Git hooks (installed by `graphify hook install`)
**File:** `.git/hooks/post-commit` and `.git/hooks/post-checkout`
**What:** Automatically runs `graphify update .` after every `git commit` or `git checkout`
**Trigger:** Git operations
**Evidence from session:** When we ran `git checkout -b graphify`, the terminal printed:
```
[graphify] Branch switched - launching background rebuild
```
This happened because `graphify claude install` also installed the git hooks automatically.

### Integration 3 — CLAUDE.md rules (installed by `graphify claude install`)
**File:** `CLAUDE.md`
**What:** Written instructions telling Claude HOW to use the graph (query first, read files second, etc.)
**Trigger:** Claude reads CLAUDE.md at the start of every session

### Summary table

| Integration | File | Installed by | Triggered by |
|---|---|---|---|
| Claude Code hook | `.claude/settings.json` | `graphify claude install` | Claude tool calls |
| Git hooks | `.git/hooks/post-commit` | `graphify claude install` (or `graphify hook install`) | `git commit`, `git checkout` |
| CLAUDE.md rules | `CLAUDE.md` | `graphify claude install` | Claude session start |

---

## 5. Core Commands

### `graphify update .` — Rebuild graph (free, AST-only)
```powershell
graphify update .
```
- Run after any code change
- No API key needed
- ~2-5 seconds for a 49-file repo
- Rewrites `graph.json`, `graph.html`, `GRAPH_REPORT.md`

### `graphify query "question"` — Search the graph
```powershell
graphify query "How does RBAC pre-filtering work?"
graphify query "cache key construction role-bound"
graphify query "authentication boundary enforcement"
```
- Case insensitive
- Plain English, any phrasing
- Uses fuzzy matching against node labels → BFS traversal
- Default budget: 2,000 tokens of output
- Add `--budget 1500` to limit, `--budget 5000` to expand

### `graphify explain "symbol"` — Expand one node
```powershell
graphify explain "MockRAGClient"
graphify explain "UserContext"
```
- Shows the node's source file, line number, community, degree (edge count)
- Lists all connections (incoming and outgoing)
- Handles duplicate node names by picking the first match

### `graphify affected "symbol" --depth 2` — Blast radius
```powershell
graphify affected "HaikuJudge" --depth 2
graphify affected "redaction_guard" --depth 2
```
- Reverse traversal — finds everything that depends on a node
- Use BEFORE editing anything to know the impact
- Requires a **unique** node name (see Common Errors)

### `graphify path "A" "B"` — Connection between two concepts
```powershell
graphify path "semantic cache" "RBAC"
graphify path "HaikuJudge" "test_rbac_redteam.py"
```
- Finds the shortest path between two nodes in the graph
- Reveals hidden cross-cutting dependencies

### `graphify extract . --backend gemini` — Full LLM enrichment
```powershell
$env:GEMINI_API_KEY = "your-key-here"
graphify extract . --backend gemini
```
- Runs AST extraction PLUS sends docs/markdown to Gemini for semantic understanding
- Creates semantic edges that bridge vocabulary gaps
- One-time cost: ~$0.06 for a 49-file repo with Gemini
- Result persists in `graph.json` — future `graphify update .` is still free

### `graphify watch .` — Auto-rebuild on file save
```powershell
graphify watch .
```
- Leave running in a terminal
- Rebuilds graph every time you save a file
- Useful during active development sessions

### `graphify hook install` — Auto-rebuild on git commit
```powershell
graphify hook install
```
- Installs post-commit and post-checkout git hooks
- Graph rebuilds automatically in the background after every commit
- You never have to remember to run `graphify update .`

---

## 6. Understanding the Outputs

### `graphify-out/graph.json`
The raw data. Contains all nodes, edges, community assignments, god node rankings. Every other output is derived from this file. Version-control this file — it's the graph itself.

### `graphify-out/graph.html`
Interactive D3 force-directed visualization. Open in any browser. Click nodes to see their connections. Zoom, pan, drag. The visual layout re-randomizes on each load (that's normal — D3 force simulation). This file is a Canvas renderer, not SVG.

### `graphify-out/GRAPH_REPORT.md`
Human-readable summary. Sections:
- **Corpus Check** — file count, word count
- **Summary** — node/edge/community counts, extraction percentages
- **Graph Freshness** — which commit it was built from
- **God Nodes** — most-connected symbols (highest blast radius)
- **Surprising Connections** — unexpected cross-file relationships
- **Communities** — clusters of related nodes with cohesion scores
- **Knowledge Gaps** — isolated nodes, thin communities

### `graphify-out/.graphify_analysis.json`
Machine-readable version of the report. Contains the full community membership list, cohesion scores per community, god node rankings with exact edge counts, and surprising connections with confidence ratings. Used by the `graphify` CLI internally.

### What to commit vs ignore
```gitignore
# Add to .gitignore
graphify-out/cache/         # machine-generated, changes every rebuild
.claude/settings.local.json # local permissions, not for sharing

# Commit these
graphify-out/graph.json     # the graph — this is the valuable artifact
graphify-out/graph.html     # the visualization
graphify-out/GRAPH_REPORT.md # the report
CLAUDE.md                   # the rules for Claude
.claude/settings.json       # the PreToolUse hook
```

---

## 7. AST-Only vs Gemini API Extraction

### What AST extraction does (free)

Tree-sitter parses your code files and extracts:
- Function and class definitions → nodes
- Function calls → `--calls-->` edges
- Import statements → `--imports-->` edges
- Parameter types → `--references-->` edges

Markdown files get heading structure only — section titles become nodes, but the content between them is not understood.

### What API extraction adds ($0.06 for 49 files)

Gemini reads your files as text and adds:
- `--contains-->` edges between section headings and their content
- Concept nodes for technology terms (`efficient_filter`, `crag`, `rbac`, `redis_stack`)
- Cross-file `--references-->` edges found in prose
- `--shares_data_with-->` edges between data structures used together

### Real numbers from this session

| Metric | AST only | Gemini enriched | Change |
|---|---|---|---|
| Nodes | 865 | 885 | +20 |
| Edges | 1,188 | 1,248 | +60 |
| Communities | 80 | 73 | -7 (better clustering) |
| Cost | $0.00 | $0.06 | one-time |
| API tokens | 0 | 82,988 in / 6,187 out | — |

### Query result comparison

**Query:** `"authentication boundary enforcement"`

| | AST only | Gemini enriched |
|---|---|---|
| Start nodes | Test string fragments that contained "boundary" | "3.3 Three Enforcement Layers", "4.3 RBAC — Three Enforcement Layers" |
| Result quality | Test class names only | Layer 1/2/3 RBAC nodes, `redaction_guard()`, DSL query, Mathematical Proof |
| Why | "authentication" ≠ "RBAC" (word mismatch) | Gemini understood they mean the same concept |

### Which backend to use

| Backend | Cost | Best for |
|---|---|---|
| `graphify update .` | Free | After code changes, daily use |
| `--backend gemini` | ~$0.06 one-time | Doc-heavy repos, cross-vocabulary queries |
| `--backend claude` | ~$0.10 one-time | If you have Anthropic API key |
| `--backend openai` | ~$0.10 one-time | If you have OpenAI key |

**Important:** AWS Bedrock is NOT supported. Graphify only supports direct API keys (Anthropic, Gemini, OpenAI, etc.).

### When to re-run API extraction

| Situation | Command |
|---|---|
| Code change (function renamed, new test) | `graphify update .` (free) |
| New design doc added | `graphify extract . --backend gemini` |
| Large refactor, many files changed | `graphify extract . --backend gemini --force` |
| First time setup | `graphify extract . --backend gemini` |

---

## 8. Can Claude CLI Replace the API Key?

**Yes — for interactive use.** Here is exactly what each approach does:

```
Terminal only (no API, no Claude):
  graphify query "authentication boundary enforcement"
  → fuzzy match → "boundary" found in test strings
  → BFS returns: test class names
  → No synthesis
  → You read raw node dumps

Terminal + Gemini API (graphify extract):
  graphify extract . --backend gemini  [one-time]
  graphify query "authentication boundary enforcement"
  → fuzzy match → "RBAC enforcement layers" found (semantically)
  → BFS returns: Layer 1, Layer 2, redaction_guard(), DSL query
  → No synthesis
  → You read raw node dumps (but relevant ones)

Ask Claude (me) instead of terminal:
  You: "How does RBAC pre-filtering work?"
  Claude runs: graphify query "RBAC pre-filtering"
  Claude knows: "authentication" = "RBAC" = "efficient_filter" (language model)
  Claude reads: design/module-4-ops-security.md sections directly
  Claude writes: a structured prose answer with line references
  → Full synthesis
  → You get a human-readable explanation
```

### The one thing Claude cannot do that API extraction can

`graphify extract` writes semantic edges **permanently into graph.json**:
```
"redaction_guard()" --implements--> "access control enforcement boundary"
```
This annotation stays in the graph forever. Next time anyone runs `graphify query` in the **terminal** — without Claude — it finds the right nodes.

Claude's understanding exists only in the conversation session. The graph itself stays vocabulary-limited.

### Summary

| Scenario | Use |
|---|---|
| You're working alone with Claude Code | Ask Claude — equivalent to API enrichment |
| Teammates use graphify in terminal | Run `graphify extract` once to enrich the graph |
| CI/CD pipeline queries the graph | Run `graphify extract` once to enrich the graph |
| Quick question while coding | Ask Claude in Claude Code |

---

## 9. Common Errors and Fixes

### Error: `No unique node match for UserContext`

**Cause:** Multiple nodes have the same name. `UserContext` appears in both `tests/conftest.py` and `tests/test_rbac_redteam.py`.

**The `affected` command requires a unique match.**

**Fix — use `explain` instead** (handles duplicates by picking first match):
```powershell
graphify explain "UserContext"
```

**Or — use `query` for a broader traversal** (handles duplicates fine):
```powershell
graphify query "UserContext callers dependencies"
```

**Or — use the full node ID** if you know it from `GRAPH_REPORT.md`:
```powershell
graphify affected "tests_conftest_usercontext" --depth 2
```

### Error: `ModuleNotFoundError: No module named 'graphify'` after install

**Cause:** Multiple Python versions. `pip install` went to Python 3.10 but `python` runs Python 3.13.

**Fix:**
```powershell
# Always use python -m pip, not pip
python -m pip install graphifyy
python -m pip show graphifyy   # verify it installed to the right Python
```

### Error: `graphify query` returns irrelevant nodes

**Cause:** Vocabulary mismatch — your question uses different words than your codebase.

**Fixes:**
1. Use the exact words from your codebase: `graphify query "RBAC efficient_filter"` instead of `"authentication"`
2. Run `graphify extract . --backend gemini` to add semantic bridging (one-time)
3. Ask Claude Code to bridge the gap for you

### Warning: `[graphify watch] command substitution: ignored null byte in input`

This appears in git hook output and is harmless. It's a known minor issue in the graphify hook script on Windows. The graph still rebuilds correctly.

### graph.html shows nothing / blank

**Cause:** Graph is rendering but took time. The D3 force simulation runs async.

**Fix:** Wait 2-3 seconds after the page loads before interacting. The nodes start packed in the center and spread out as the simulation runs.

---

## 10. Saving the Graph as an Image

The graph is rendered on an HTML `<canvas>` element (not SVG). This matters for how you export it.

### Save as PNG (works, confirmed)

1. Open `graphify-out/graph.html` in Chrome or Edge
2. Wait for the graph to fully render and settle (~3 seconds)
3. Press **F12** → **Console** tab
4. Paste this and press Enter:

```javascript
const canvas = document.querySelector('canvas');
const a = Object.assign(document.createElement('a'), {
  href: canvas.toDataURL('image/png'),
  download: 'graph.png'
});
a.click();
```

Downloads `graph.png` to your Downloads folder instantly.

### Higher resolution export

Zoom in with **Ctrl + `+`** several times before running the command. The canvas captures at whatever zoom level is active.

### Why SVG export fails

`document.querySelector('svg')` returns `null` because the renderer uses `<canvas>`, not `<svg>`. Running `XMLSerializer` on null gives:
```
TypeError: Failed to execute 'serializeToString' on 'XMLSerializer': 
parameter 1 is not of type 'Node'
```

Canvas → PNG is the correct export path. SVG is not available without a different rendering library.

---

## 11. Day-to-Day Workflow

### Before starting any task

```powershell
# 1. Check if graph is stale
# Open GRAPH_REPORT.md and check "Built from commit"
# Compare with: git rev-parse HEAD

# 2. If stale, rebuild (free, 2 seconds)
graphify update .

# 3. Query what you're about to touch
graphify query "the area I'm working in"
```

### Before changing code

```powershell
# Find the blast radius FIRST
graphify explain "FunctionNameIAmChanging"
graphify query "FunctionNameIAmChanging callers tests"
```

### For god nodes (highest blast radius in this repo)

Always use `graphify explain` or `graphify query` — never `graphify affected` (too many duplicates):

| Node | Edge count | Where defined |
|---|---|---|
| `UserContext` | 49 | tests/conftest.py:95 |
| `ChunkMeta` | 45 | tests/conftest.py:106 |
| `MockRAGClient` | 41 | tests/conftest.py:812 |
| `HaikuJudge` | 30 | tests/conftest.py:522 |
| `RAGResponse` | 25 | tests/conftest.py:130 |
| `TelemetrySink` | 25 | tests/conftest.py:773 |

If you change any of these, run the full test suite — not just the affected file.

### After changing code

```powershell
graphify update .   # refresh graph, free, no API call
```

If you also changed markdown/docs:
```powershell
$env:GEMINI_API_KEY = "your-key"
graphify extract .  # semantic refresh, ~$0.01 incremental
```

### For onboarding / understanding an unfamiliar area

```powershell
graphify query "what does X do"           # broad orientation
graphify query "X callers dependencies"   # who uses it
graphify path "X" "Y"                     # how two things connect
graphify explain "SpecificSymbol"         # deep dive on one node
```

---

## 12. The Benefit — Concrete Numbers

From this actual session, comparing graphify query to manual file-grepping:

| Question | Without graphify | With graphify |
|---|---|---|
| "What tests depend on UserContext?" | grep 8 files, read 200 lines | `graphify explain "UserContext"` — 0.5 seconds |
| "How is cache connected to RBAC?" | Open 3 design docs, cross-reference | `graphify path "semantic cache" "RBAC"` — 1 second |
| "What's the blast radius of changing ChunkMeta?" | Read all 9 test files manually | `graphify explain "ChunkMeta"` — 0.5 seconds |
| "Where does RBAC enforcement happen?" | Search codebase, maybe miss design docs | `graphify query "RBAC enforcement"` — 1 second |

### Where graphify adds the most value

- **Large repos (500+ files):** The time savings compound. A 5,000-file repo takes hours to manually navigate; graphify covers it in seconds.
- **Cross-vocabulary codebases:** When design docs, code, and tests use different words for the same concept (this repo: "authentication boundary" vs "RBAC" vs `efficient_filter`).
- **New team member onboarding:** Instead of 2 weeks of file reading, one `graphify query` session gives a structural overview.
- **Before refactoring:** `graphify affected` (or `graphify explain`) reveals dependencies you didn't know existed.
- **Code review:** `graphify path "changed file" "test file"` confirms test coverage paths.

### Where graphify adds less value

- Tiny repos (< 10 files) — just read the files
- Repos where your questions match the exact code vocabulary (no vocabulary gap)
- Single isolated bug fixes where you already know the file

---

## 13. Full Q&A Reference

These are real questions asked during the learning session, with complete answers.

---

**Q: Is `graphify query` case sensitive? Can I ask anything?**

No, it is not case-sensitive. You can ask in plain English. However, it is not a Q&A system — it uses fuzzy text matching against node labels, not semantic understanding. Without API enrichment, "authentication" will not find "RBAC" because the words don't overlap. With API enrichment, it will.

---

**Q: Does graphify use NLP or LLM to detect my question?**

Neither — without an API key. It uses `rapidfuzz` (fuzzy string matching) to find the closest node labels to your question words, then BFS graph traversal. It is fundamentally a graph search tool, not a language model. The `INFERRED` edges in the graph (confidence ~0.52) come from heuristics, not language models. Only when you run `graphify extract --backend gemini` does an actual LLM get involved — and that LLM is external (Gemini/Claude/OpenAI), not built into graphify.

---

**Q: I ran `graphify query "What does the LLM-as-judge do?"` — how can graphify answer that?**

It cannot write an answer — it returns relevant nodes. Graphify would fuzzy-match "LLM-as-judge" against node labels, find the `HaikuJudge` node (whose label contains "LLM-as-judge calls"), and return its 30 connected nodes and edges. You (or Claude) then synthesize the answer from those nodes. Graphify is the search engine; the answer is your synthesis.

---

**Q: `graphify affected "UserContext" --depth 2` returns "No unique node match for UserContext." Why?**

Because `UserContext` appears as a node in two different files: `tests/conftest.py:95` and `tests/test_rbac_redteam.py:70`. The `affected` command requires a unique match. Use `graphify explain "UserContext"` instead (which picks the first match), or `graphify query "UserContext"` (which handles duplicates).

---

**Q: What does `graphify affected "<symbol>"` mean? What is `<symbol>`?**

`<symbol>` is a placeholder notation — angle brackets mean "replace this with your actual value." It is programming documentation convention. You would run:
```powershell
graphify affected "HaikuJudge" --depth 2
graphify affected "build_cache_key" --depth 2
```
Any function name, class name, or node label from the graph is valid input.

---

**Q: Does `graphify hook install` add things to `.claude/settings.json`?**

No. These are two completely separate hooks:
- **`graphify claude install`** → writes PreToolUse hook to `.claude/settings.json` (Claude Code integration)
- **`graphify hook install`** → writes post-commit/post-checkout hooks to `.git/hooks/` (git integration)

They solve different problems. `graphify claude install` makes Claude consult the graph when answering questions. `graphify hook install` makes the graph auto-rebuild after every git commit. You can have both, either, or neither.

---

**Q: Can graphify teach me NLP?**

Partially — but it is not an NLP tool. What graphify genuinely teaches:
- **Tree-sitter AST parsing** — how code is converted to a syntax tree where functions, classes, and calls become structured data
- **Graph construction** — turning a codebase into nodes and edges
- **Community detection** — Louvain algorithm, how clusters of related code are identified
- **Betweenness centrality** — why some nodes (god nodes) are the most dangerous to change
- **BFS/DFS traversal** — how queries navigate the graph
- **MinHash (datasketch)** — probabilistic near-duplicate detection

What it does NOT teach: semantic understanding, embeddings, transformers, or language model concepts. For NLP, look at spaCy, Hugging Face, or LangChain tutorials instead.

---

**Q: If I use an API key, does `graphify query` behavior change?**

Yes — significantly. With the API key you first run `graphify extract . --backend gemini` (one-time). This adds semantic edges to graph.json. After that, `graphify query` can find nodes by meaning, not just matching words.

Example: `graphify query "authentication boundary enforcement"` before enrichment matched test string fragments; after enrichment it directly found the RBAC design sections, the `redaction_guard()` function, and the mathematical proof of why post-filtering leaks — because Gemini understood "authentication boundary" means "RBAC enforcement layer."

---

**Q: Instead of running `graphify query` in the terminal, can I ask Claude CLI and get the same result as having an API key?**

For interactive use, yes — and in some ways better. Claude Code (me) bridges vocabulary gaps using language model understanding, reads the actual source files to fill in what the graph returns as just node titles, and synthesizes a prose answer. This covers the same gap that API enrichment covers.

The difference: Claude's understanding exists only in the conversation. API enrichment writes semantic edges permanently into graph.json, so future terminal queries and teammates also benefit — without Claude.

---

**Q: What files did graphify create/modify, vs what did Claude create?**

**Created by graphify CLI (deterministic, automatic):**
- `graphify-out/graph.json`
- `graphify-out/graph.html`
- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/manifest.json`
- `graphify-out/.graphify_analysis.json`
- `graphify-out/.graphify_labels.json`
- `graphify-out/.graphify_root`
- `CLAUDE.md` (the `## graphify` section)
- `.claude/settings.json` (the PreToolUse hook)

**Created by Claude (synthesized from graph data):**
- `docs/PROJECT_OVERVIEW.md`
- `docs/ARCHITECTURE.md`
- `docs/MODULE_MAP.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/TODO_RISKS.md`
- `docs/GRAPHIFY_API_ENRICHMENT.md`
- `CLAUDE.md` (the `## Repository understanding rule` section added after graphify's section)

The `docs/` content was derived from the graphify outputs — the god node table, community-to-file mappings, and risk flags all came from `GRAPH_REPORT.md`. Claude restructured them into human-friendly cross-linked documents.

---

**Q: Do I need to re-run graphify after changing the repo?**

Yes — but cheaply:
- Code change → `graphify update .` (free, ~2 seconds)
- New docs added → `graphify extract . --backend gemini` (~$0.01 incremental)
- Already on commit hook → it runs automatically in the background

The `GRAPH_REPORT.md` header shows which commit the graph was built from. Compare with `git rev-parse HEAD` to know if it's stale.

---

**Q: How do I save the graph as an image?**

The graph is rendered on a `<canvas>` element, not SVG. Save as PNG from the browser console:

```javascript
const canvas = document.querySelector('canvas');
const a = Object.assign(document.createElement('a'), {
  href: canvas.toDataURL('image/png'),
  download: 'graph.png'
});
a.click();
```

SVG export does not work because there is no SVG element in the page (`document.querySelectorAll('svg').length === 0`).

---

## Quick Reference Card

```
SETUP (once per repo)
  python -m pip install graphifyy
  graphify claude install          # Claude Code + git hooks + CLAUDE.md
  graphify update .                # Build initial graph (free)
  $env:GEMINI_API_KEY = "..."
  graphify extract . --backend gemini   # Semantic enrichment (optional, ~$0.06)

DAILY USE
  graphify query "plain English question"    # search
  graphify explain "SymbolName"              # expand one node
  graphify path "ConceptA" "ConceptB"        # find connection
  graphify update .                          # refresh after code changes

BEFORE EDITING
  graphify explain "ThingIAmChanging"        # see blast radius
  graphify query "ThingIAmChanging callers"  # find all users

EXPORT
  Open graph.html in browser → F12 Console →
  const canvas = document.querySelector('canvas');
  const a = Object.assign(document.createElement('a'),
    {href: canvas.toDataURL('image/png'), download: 'graph.png'});
  a.click();

REMEMBER
  - graph.json is the valuable artifact — commit it
  - graphify-out/cache/ is noise — add to .gitignore
  - "authentication" ≠ "RBAC" without API enrichment
  - graphify does not write prose answers — that is your job (or Claude's)
  - God nodes (UserContext, ChunkMeta, MockRAGClient) = highest blast radius
```
