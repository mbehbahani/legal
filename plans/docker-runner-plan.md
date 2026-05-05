# docker-runner — Planning Phase

## 1. Deliverables (file-by-file)

- `docker/Dockerfile` — multi-stage Python 3.12-slim image: `builder` stage compiles wheels (`faiss-cpu`, `tiktoken`, `rank-bm25`); `runtime` stage is slim, non-root `app` user, `tini` as PID 1.
- `docker/docker-compose.yml` — base stack: `app`, `opensearch` (single-node 2.18+, security plugin enabled, Lucene k-NN), `redis-stack`, `jaeger` (all-in-one, OTLP on 4317), `minio` (corpus blob store). **NO local LLM** — `app` calls AWS Bedrock for Haiku + Cohere embed/rerank. Single internal bridge network, named volumes, healthchecks on every service.
- `docker/compose.override.yml` — dev affordances: source bind-mount, `pytest` reload, debug ports exposed (5678 debugpy, 9200 OpenSearch, 5601 OpenSearch Dashboards, 16686 Jaeger UI, 8001 Redis Insight), looser CPU/mem caps.
- `docker/.dockerignore` — excludes `.git`, `corpus/raw`, `__pycache__`, `.venv`, `notebooks`, `*.md` to keep build context <50 MB.
- `docker/healthcheck/qdrant.sh`, `redis.sh`, `langfuse.sh`, `ollama.sh` — curl / redis-cli probes returning non-zero until ready; used by both compose `healthcheck` blocks and the `run-eval.sh` gate.
- `scripts/run-eval.sh` — orchestrator: `compose build` → `compose up -d` → poll healthchecks → `compose exec app pytest -v --junitxml=reports/junit.xml` → on failure capture logs → write `reports/test-results.md`.
- `scripts/debug-shell.sh` — `compose exec app bash` with env preloaded for interactive triage.
- `scripts/seed-corpus.sh` — pushes sample legal fixtures into `minio`, triggers ingestion, warms Qdrant + semantic cache before the eval suite runs.

## 2. Key infra decisions (leaning)

1. **Base image**: `python:3.12-slim` multi-stage. `builder` carries build-essential for native wheels (boto3, opensearch-py); `runtime` is slim + non-root. Small attack surface.
2. **Vector store**: **OpenSearch 2.18** single-node with security plugin + Lucene k-NN engine. `plugins.security.disabled=false` so DLS tests are meaningful; demo certs auto-generated on first boot. Maps to AWS-managed OpenSearch Service in prod.
3. **Redis flavor**: **Redis Stack 7.4** (RediSearch + vector field). One service powers the semantic cache (Module 4) plus rate-limit/session.
4. **Observability**: **Jaeger all-in-one** (`jaegertracing/all-in-one:1.62`, OTLP gRPC on 4317, UI on 16686). In-memory storage for dev; prod points at Cassandra or OpenSearch backend.
5. **LLM/embed/rerank source**: **AWS Bedrock direct from app container** (Haiku 4.5 + Cohere embed-multilingual-v3 + Cohere rerank-v3-5:0). Creds via env vars from `.env`. `EVAL_LLM_PROVIDER=bedrock` default; `=mock` for offline unit tests.
6. **Resource limits**: app 2 CPU / 4 GB; OpenSearch 4 GB heap (`-Xms4g -Xmx4g`); Redis 1 GB; Jaeger 512 MB. `ulimits.memlock=-1` and `vm.max_map_count=262144` for OpenSearch.
7. **Networking & secrets**: one bridge net `rag-net`; no host port publishing in the prod override. AWS creds via `.env` + compose `env_file` (gitignored); IAM role policy documented in `docker/IAM-POLICY.md` (least-privilege: `bedrock:InvokeModel` on the three model IDs only).

## 3. Open questions

- Host specs (RAM / CPU / disk)? Assuming Win11 Docker Desktop with WSL2; OpenSearch needs ≥6 GB free RAM.
- AWS creds in CI: GitHub Actions OIDC + assume-role, or static keys in repo secrets?
- Local OpenSearch sufficient for tests, or does CI need to point at a real Amazon OpenSearch domain for fidelity?
- Is `corpus/raw` provided, or do we synthesize fixtures inside `seed-corpus.sh` (default: synthesize ~250)?

## 4. Dependencies

- **Inbound**: final picks from vector-db-architect (Qdrant vs Weaviate), caching-architect (Redis Stack confirm + similarity threshold), observability-architect (Langfuse vs Phoenix). Test suite + fixtures from rag-evaluation-engineer.
- **Outbound**: `reports/test-results.md` (pass/fail matrix, Ragas/DeepEval scores, latency stats, container log excerpts) consumed by report-compiler.

## 5. Effort + likely failure modes

- **Effort**: ~1.5 days (0.5 Dockerfile/compose, 0.5 healthchecks + scripts, 0.5 debug loop).
- **Top 3 anticipated failures**:
  1. **OpenSearch security-plugin first-boot race** — demo cert generation + admin password setup races with pytest. Mitigation: `/_cluster/health?wait_for_status=yellow&timeout=60s` healthcheck + retry wrapper; `OPENSEARCH_INITIAL_ADMIN_PASSWORD` set in env.
  2. **Bedrock throttling** during the eval run — Haiku has per-region TPM quotas. Mitigation: adaptive retry config in boto3 (`Config(retries={'mode':'adaptive','max_attempts':10})`); concurrency cap on the test runner.
  3. **AWS credential not reaching container** — silent fallback to anonymous and 403 from Bedrock. Mitigation: app startup probe pings `sts:GetCallerIdentity` and logs the ARN before serving traffic.
