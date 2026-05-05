# Launch Prompt — Paste this into a fresh Claude Code session

> Open Claude Code in `d:\AWS\Legal\` and paste the block below. The agents in `.claude/agents/` will then be registered and invokable by name.

---

```
You are continuing work on the Tax Authority RAG architecture assignment in this directory.

CONTEXT — read these first, in this order:
1. d:\AWS\Legal\assignment — the original task
2. d:\AWS\Legal\plans\MASTER-PLAN.md — the source of truth for stack, locked decisions, and execution sequence
3. d:\AWS\Legal\plans\*-plan.md — five per-agent plans
4. d:\AWS\Legal\.claude\agents\*.md — seven agent charters (rag-retrieval-architect, agentic-rag-designer, mlops-security-architect, legal-domain-reviewer, rag-evaluation-engineer, docker-runner, report-compiler, process-report-author)

LOCKED DECISIONS (do not re-litigate):
- Scope: evidence-backed — all 6 phases run end-to-end.
- All 7 open questions resolved to defaults per MASTER-PLAN.md section E.
- Stack: AWS Bedrock (Claude Haiku 4.5 via cross-region inference profile us.anthropic.claude-haiku-4-5-20251001-v1:0, Cohere embed-multilingual-v3, Cohere rerank-v3-5:0), Amazon OpenSearch (Lucene k-NN with efficient_filter), Redis Stack, Jaeger. Verified working in us-east-1 against AWS account 780822965578.
- Currently authenticated as root credentials — fine for the assignment; flag if a least-privilege IAM user becomes blocking.

EXECUTION SEQUENCE:
Phase 1 (parallel, 3 agents): rag-retrieval-architect, agentic-rag-designer, mlops-security-architect → drafts in d:\AWS\Legal\design\
Phase 2: legal-domain-reviewer reads all three, appends ⚠️/❌ findings in-place
Phase 3: rag-evaluation-engineer writes the test suite under d:\AWS\Legal\tests\
Phase 4: docker-runner builds the docker stack, executes the suite, debugs failures, writes d:\AWS\Legal\reports\test-results.md
Phase 5: report-compiler produces d:\AWS\Legal\design\FINAL-rag-architecture.md (technical deliverable for design reviewers)
Phase 6: process-report-author produces d:\AWS\Legal\reports\PROCESS-REPORT.md (methodology deliverable for reviewers interested in the multi-agent architecture itself)

TIMING CAPTURE (mandatory — Phase 6 depends on it):
Before each agent invocation, write a JSONL row to d:\AWS\Legal\reports\agent-timings.jsonl with: {agent, phase, start_iso, end_iso, duration_ms, tokens_in, tokens_out, status}. Without this the process-report cannot reconstruct the span empirically.

GUARDRAILS:
- Sub-agents cannot write files in this harness; have them return content in their result and persist it from the orchestrator.
- Never weaken or skip a test to make CI green — fix the underlying issue or document why it cannot pass.
- Never bake AWS credentials into a Docker image — use env_file with a gitignored .env.
- Cross-region inference profile (us. prefix) is mandatory for Haiku 4.5 — direct on-demand model IDs are rejected.

DELIVERABLES at the end:
- d:\AWS\Legal\design\FINAL-rag-architecture.md — the technical architecture document (12–20 pages, traceability checklist included)
- d:\AWS\Legal\reports\PROCESS-REPORT.md — the agent-architecture methodology report (6–10 pages, mermaid diagrams, real timing data)
- d:\AWS\Legal\tests\ — runnable suite
- d:\AWS\Legal\docker\ + scripts\ — runnable stack
- d:\AWS\Legal\reports\test-results.md — empirical validation

START BY:
1. Reading MASTER-PLAN.md and confirming the locked sequence.
2. Creating a TaskCreate plan covering all 6 phases.
3. Writing the first agent-timings.jsonl entry.
4. Launching Phase 1 (the three design agents in parallel).

Show me the task plan and Phase 1 launch summary, then proceed.
```

---

## Why a fresh session

Custom agents under `.claude/agents/` are registered by Claude Code at session start. The current session was opened before those files existed, so the harness only knows about built-in subagent types. A fresh session will load them and let the orchestrator invoke them by name (`subagent_type: "rag-retrieval-architect"` etc.) instead of falling back to `general-purpose`.

## What you'll get

| Document | Audience | Pages |
|---|---|---|
| `design/FINAL-rag-architecture.md` | Reviewers of the *design* (technical evaluators) | 12–20 |
| `reports/PROCESS-REPORT.md` | Reviewers of the *agent architecture* (interested in the multi-agent system that produced the design) | 6–10 |

The process report is exactly what you asked for: agent roster, mermaid architecture diagram, gantt timeline, decision provenance table, real Bedrock token/cost numbers, cross-agent handoffs, quality gates, and limitations — written for non-engineering reviewers.
