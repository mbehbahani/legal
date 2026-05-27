# Development Workflow

## Prerequisites
- Python 3.13 (the `tests/__pycache__/` artifacts are `cpython-313`)
- Docker Desktop (for the compose stack)
- AWS credentials with Bedrock access in `us-east-1` (Cohere embed/rerank + Claude Haiku 4.5)
- `graphifyy` installed (`python -m pip install graphifyy`) for repo-understanding queries

## Repo-understanding workflow (graphify)
Before editing or answering architectural questions, query the graph instead of grepping blindly.

```bash
# Find files / symbols connected to a concept
graphify query "How does RBAC pre-filtering work?"

# Expand a specific symbol and its neighbors
graphify explain "MockRAGClient"

# Find what's downstream of a node (reverse traversal)
graphify affected "UserContext" --depth 2

# Shortest path between two concepts
graphify path "semantic cache" "RBAC"

# Refresh after code changes (AST-only, no API key)
graphify update .
```

The graph lives at [graphify-out/graph.json](../graphify-out/graph.json) with a human report at [graphify-out/GRAPH_REPORT.md](../graphify-out/GRAPH_REPORT.md) and an interactive HTML view at [graphify-out/graph.html](../graphify-out/graph.html).

A PreToolUse hook in [.claude/settings.json](../.claude/settings.json) (installed via `graphify claude install`) makes Claude Code consult the graph automatically before answering codebase questions.

## Running the evaluation stack
```bash
# 1. Bring up dependencies
docker compose -f docker/docker-compose.yml up -d

# 2. Seed the synthetic corpus into OpenSearch
bash scripts/seed-corpus.sh

# 3. Run the full evaluation suite
bash scripts/run-eval.sh

# 4. Assert promotion-gate thresholds (used in CI)
python scripts/assert_thresholds.py
```

Healthchecks for each service live in [docker/healthchecks/](../docker/healthchecks/).

## Test layout
All tests are pytest-based and share fixtures in [tests/conftest.py](../tests/conftest.py). Each test file maps 1:1 to a quality dimension — see [MODULE_MAP.md](MODULE_MAP.md) for the table.

Run a single dimension:
```bash
pytest tests/test_rbac_redteam.py -v
```

## Changing code — the loop
1. **Query the graph first** — `graphify query "<what you're touching>"` to identify affected modules.
2. Make the smallest safe change.
3. Run the affected test file (`pytest tests/test_<X>.py`).
4. Run the full suite if you touched anything in [tests/conftest.py](../tests/conftest.py), a god node, or a cross-community bridge.
5. `graphify update .` to refresh the graph (no API cost).
6. Update [docs/](.) if you changed architecture, added a module, or shifted the build/run story.

## God nodes — handle with care
These have the largest blast radius (edge count in parentheses):
- `UserContext` (49) — identity envelope; every test depends on it
- `ChunkMeta` (45) — retrieved-chunk record
- `MockRAGClient` (42) — pipeline stub used by every test file
- `HaikuJudge` (30) — LLM-as-judge wrapper
- `RAGResponse` (25) — pipeline output contract
- `TelemetrySink` (22) — observability sink

Always `graphify affected "<node>" --depth 2` before changing one.
