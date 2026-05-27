# Risks & TODOs

Open risks and known gaps. Sourced from [graphify-out/GRAPH_REPORT.md](../graphify-out/GRAPH_REPORT.md) "Knowledge Gaps" and "Suggested Questions" sections, plus the repo's own design-review findings.

## Graph-derived risks

### Inferred-edge confidence
The graph contains **194 INFERRED edges (avg confidence 0.52)** — model-reasoned relationships, not AST-extracted. Audit candidates:
- `UserContext` — 42 inferred edges (e.g. with `str` and `ChunkMeta`)
- `ChunkMeta` — 41 inferred edges (e.g. with `int` and `float`)
- `MockRAGClient` — 36 inferred edges
- `HaikuJudge` — 23 inferred edges

Many inferred edges look like primitive-type pollution (`float --uses--> UserContext` from a fixture signature). Worth pruning before relying on them.

### Isolated nodes
**294 isolated nodes** (≤1 connection) detected. Most are stringly typed config tokens (`npm`, `enabledMcpjsonServers`, `PreToolUse`, `allow`, `app.sh script`...). Either:
- they're genuinely standalone and fine, or
- the extractor missed an edge into them.

Spot-check anything that looks like a real abstraction stranded in the isolated list.

### Cross-community bridges (high betweenness)
These nodes connect otherwise-separate parts of the system. Changes here have the widest blast radius:
- `UserContext` (betweenness 0.070) — bridges 11 communities
- `ChunkMeta` (0.037) — bridges 10 communities
- `MockRAGClient` (0.028) — bridges 8 communities

## Domain-review findings (from the design phase)
See [design/](../design/) and the per-check files (Community 27 in the graph). Open checks worth re-verifying:
- **Citation Format (Check 1)** — anchor depth (`artikel/lid/onderdeel/sub`) must be enforced, not just suggested
- **Hierarchy Depth (Check 2)** — chunk metadata schema vs. real Belastingdienst document structure
- **Superseded / Consolidated Versions (Check 4)** — `valid_from`/`valid_to` correctness across legislative revisions
- **FIOD Classification (Check 5)** — leakage paths into helpdesk role
- **Multilinguality (Check 6)** — embed-multilingual-v3 coverage on Dutch + EN legal text
- **Legal Counsel Role (Check 7)** — escalation contract
- **Cache Poisoning / Tax-Year Ambiguity (Check 8)** — proven role-bound key; year scoping still worth a fresh red-team pass

## Repository maturity caveats (from README)
- The repo is **architecture + evaluation harness**, not a production deployment. The Docker stack and tests are designed to *prove* the design, not to serve traffic.
- The evaluation suite uses a `MockRAGClient` deterministic stub plus selective real-Bedrock runs ([reports/test-results.md](../reports/test-results.md)). Coverage of real Bedrock paths is partial.

## Process / collaboration TODOs
- Refresh this file when `graphify update .` reveals new isolated nodes or god nodes.
- When fixing a domain-review finding, link the commit here and remove the bullet.
