# Module Map

Where to find each concern. Derived from [graphify-out/GRAPH_REPORT.md](../graphify-out/GRAPH_REPORT.md) community structure. Run `graphify explain "<concept>"` for any entry below to expand it.

## Design docs (the "what")
| Concern | File |
|---|---|
| Consolidated architecture | [design/FINAL-rag-architecture.md](../design/FINAL-rag-architecture.md) |
| Ingestion + retrieval (modules 1–2) | [design/module-1-2-retrieval.md](../design/module-1-2-retrieval.md) |
| Agentic / CRAG (module 3) | [design/module-3-agentic.md](../design/module-3-agentic.md) |
| Ops + security (module 4) | [design/module-4-ops-security.md](../design/module-4-ops-security.md) |

## Tests (the "proof")
| Test concern | File | Backing community |
|---|---|---|
| Shared fixtures (mock pipeline, judges, telemetry, OpenSearch/Redis clients) | [tests/conftest.py](../tests/conftest.py) | C2, C20 |
| RBAC red-team (FIOD leakage, prompt injection, cross-role cache poisoning) | [tests/test_rbac_redteam.py](../tests/test_rbac_redteam.py) | C0 |
| Citation accuracy (zero-hallucination, anchor depth) | [tests/test_citation_accuracy.py](../tests/test_citation_accuracy.py) | C6, C28 |
| Ambiguity & refusal (CRAG fallback, structured refusal contract) | [tests/test_ambiguity_refusal.py](../tests/test_ambiguity_refusal.py) | C17 |
| Latency budgets (TTFT, p95, retrieval ≤300ms, e2e ≤4s) | [tests/test_latency_budgets.py](../tests/test_latency_budgets.py) | C15 |
| Semantic cache (cosine 0.97 floor, role-bound keys, TTL by legislative date) | [tests/test_semantic_cache.py](../tests/test_semantic_cache.py) | C3 |
| Temporal correctness (`valid_from`/`valid_to`, year confusion) | [tests/test_temporal_correctness.py](../tests/test_temporal_correctness.py) | C12, C13 |
| Hybrid retrieval (BM25 + dense fusion, nDCG@k) | [tests/test_hybrid_retrieval.py](../tests/test_hybrid_retrieval.py) | C8 |
| Observability (OTel spans, Ragas gates) | [tests/test_observability.py](../tests/test_observability.py) | C9 |
| Golden Q&A pairs | [tests/golden/golden_qa.jsonl](../tests/golden/golden_qa.jsonl) | — |
| Test plan / strategy | [tests/TEST-PLAN.md](../tests/TEST-PLAN.md) | C42 |

## Infrastructure (the "how to run")
| Concern | File |
|---|---|
| Service stack (OpenSearch + Redis + Jaeger + app) | [docker/docker-compose.yml](../docker/docker-compose.yml) |
| Python runtime image | [docker/Dockerfile](../docker/Dockerfile) |
| IAM least-privilege policy | [docker/IAM-POLICY.md](../docker/IAM-POLICY.md) |
| Healthchecks | [docker/healthchecks/](../docker/healthchecks/) |
| Corpus seeding | [scripts/seed-corpus.sh](../scripts/seed-corpus.sh) + [tests/seed_opensearch.py](../tests/seed_opensearch.py) |
| Run evaluation | [scripts/run-eval.sh](../scripts/run-eval.sh) |
| Threshold assertions | [scripts/assert_thresholds.py](../scripts/assert_thresholds.py) |
| Debug shell | [scripts/debug-shell.sh](../scripts/debug-shell.sh) |

## Reports (the "did it work")
| Report | File |
|---|---|
| Test results | [reports/test-results.md](../reports/test-results.md) |
| Jaeger observability | [reports/jaeger-observability.md](../reports/jaeger-observability.md) |
| Multi-agent process report | [reports/PROCESS-REPORT.md](../reports/PROCESS-REPORT.md) |

## Agent definitions
The repo was built with seven specialized subagents in [.claude/agents/](../.claude/agents/) — see [reports/PROCESS-REPORT.md](../reports/PROCESS-REPORT.md) for the orchestration story.
