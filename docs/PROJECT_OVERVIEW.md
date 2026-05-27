# Project Overview

**Repository:** Tax Authority Enterprise RAG
**Generated with help from:** [graphify-out/GRAPH_REPORT.md](../graphify-out/GRAPH_REPORT.md) (865 nodes · 1188 edges · 80 communities)
**Last refreshed:** 2026-05-27

## What this is
A design + evaluation repository for a secure enterprise Retrieval-Augmented Generation system for a national tax authority (Netherlands Belastingdienst context). It is **not** a runnable end-user app — it is the architecture, the evaluation harness that proves it works, and the infrastructure scaffolding needed to run it.

## What's in the repo (top-level)
- [design/](../design/) — four module design docs + the consolidated `FINAL-rag-architecture.md`
- [tests/](../tests/) — pytest evaluation suite (RBAC red-team, citation accuracy, latency, semantic cache, temporal correctness, ambiguity/refusal, observability)
- [docker/](../docker/) — Dockerfile + compose stack (OpenSearch, Redis Stack, Jaeger, app)
- [scripts/](../scripts/) — seed corpus, run eval, debug shell, threshold checks
- [reports/](../reports/) — evaluation results, Jaeger trace analysis, multi-agent process report
- [plans/](../plans/) — per-agent planning artifacts used during the design phase
- [.claude/agents/](../.claude/agents/) — seven specialized subagent definitions
- [graphify-out/](../graphify-out/) — knowledge graph + report (regenerate with `graphify update .`)

## Core technology choices
| Concern | Choice |
|---|---|
| Vector store | Amazon OpenSearch Service (Lucene HNSW) with `efficient_filter` |
| Embeddings | Cohere `embed-multilingual-v3` via AWS Bedrock |
| Reranker | Cohere `rerank-v3-5:0` via AWS Bedrock |
| LLM / grader / judge | Claude Haiku 4.5 via Bedrock cross-region inference profile |
| Semantic cache | Redis Stack 7.4 (role-bound, year-scoped keys) |
| Tracing | OpenTelemetry → Jaeger |
| Orchestration | LangGraph state machine (CRAG control loop) |

## Audience for this overview
Engineers landing on the repo cold who need to know what's here and where to look next. For architecture details see [ARCHITECTURE.md](ARCHITECTURE.md). For "which file does X live in" see [MODULE_MAP.md](MODULE_MAP.md). For running the stack see [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md).
