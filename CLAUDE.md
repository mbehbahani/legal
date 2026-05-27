## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Repository understanding rule

Before answering architectural or implementation questions, use this order of precedence:

1. **Graph first** — `graphify query "<specific question>"`, `graphify explain "<symbol>"`, or `graphify affected "<symbol>"`. The graph is the canonical map of relationships.
2. **Curated docs second** — [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/MODULE_MAP.md](docs/MODULE_MAP.md), [docs/DEVELOPMENT_WORKFLOW.md](docs/DEVELOPMENT_WORKFLOW.md), [docs/TODO_RISKS.md](docs/TODO_RISKS.md). These are derived from the graph but written for humans.
3. **Raw files last** — only when 1 and 2 are insufficient. Do not open many files speculatively.

For every code change:
1. Identify affected modules with `graphify affected "<node>" --depth 2`. The god nodes (`UserContext`, `ChunkMeta`, `MockRAGClient`, `HaikuJudge`, `RAGResponse`, `TelemetrySink`) have wide blast radius — change them deliberately.
2. Make the smallest safe change.
3. Run the affected pytest file; run the full suite if a god node or `tests/conftest.py` was touched.
4. Run `graphify update .` to refresh the graph.
5. Update [docs/](docs/) if architecture, module layout, or the build/run story changed.
