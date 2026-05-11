"""
Emit representative RAG pipeline traces to Jaeger via OTLP.
Uses realistic latency numbers from Module 4 §4.2 design budget.
Run: python scripts/emit_demo_traces.py
"""
import time
import random
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

OTLP_ENDPOINT = "http://localhost:4317"

resource = Resource.create({"service.name": "tax-rag", "service.version": "1.0.0"})
provider = TracerProvider(resource=resource)
exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("tax-rag.pipeline")

SCENARIOS = [
    {
        "query": "Wat is het Box 1 belastingtarief 2024?",
        "role": "helpdesk",
        "verdict": "Relevant",
        "cache_hit": False,
        "latencies": {
            "auth": 4, "embed": 48, "hnsw": 95, "bm25": 88,
            "rrf": 9, "rerank": 187, "grade": 210, "generate": 820,
            "verify": 95, "audit": 18,
        },
    },
    {
        "query": "ECLI:NL:HR:2021:1234 arrest box 2 dividend",
        "role": "inspector",
        "verdict": "Relevant",
        "cache_hit": False,
        "latencies": {
            "auth": 5, "embed": 52, "hnsw": 101, "bm25": 91,
            "rrf": 11, "rerank": 195, "grade": 225, "generate": 1050,
            "verify": 120, "audit": 22,
        },
    },
    {
        "query": "Wat is het Box 1 belastingtarief 2024?",  # cache hit
        "role": "helpdesk",
        "verdict": "Relevant",
        "cache_hit": True,
        "latencies": {"auth": 4, "cache_lookup": 6},
    },
    {
        "query": "Hoeveel bedraagt zegelrecht Curaçao 2024?",  # refusal
        "role": "helpdesk",
        "verdict": "Irrelevant",
        "cache_hit": False,
        "latencies": {
            "auth": 4, "embed": 50, "hnsw": 98, "bm25": 90,
            "rrf": 10, "rerank": 190, "grade": 215, "audit": 19,
        },
    },
    {
        "query": "FIOD memo aandelenoverdrachten 2023",  # RBAC block
        "role": "helpdesk",
        "verdict": "RBAC_BLOCKED",
        "cache_hit": False,
        "latencies": {
            "auth": 4, "embed": 49, "hnsw": 97, "bm25": 89,
            "rrf": 10, "rerank": 188, "redaction": 8, "grade": 205, "audit": 18,
        },
    },
]

def emit_trace(scenario):
    q = scenario["query"]
    role = scenario["role"]
    verdict = scenario["verdict"]
    lats = scenario["latencies"]
    cache_hit = scenario["cache_hit"]

    with tracer.start_as_current_span("rag.request") as req_span:
        req_span.set_attribute("user.role", role)
        req_span.set_attribute("query.text", q[:80])
        req_span.set_attribute("cache.hit", cache_hit)
        req_span.set_attribute("verdict", verdict)
        req_span.set_attribute("attempt_count", 1)

        # Auth
        with tracer.start_as_current_span("auth.extract_role") as s:
            s.set_attribute("jwt.role", role)
            time.sleep(lats["auth"] / 1000)

        if cache_hit:
            with tracer.start_as_current_span("cache.lookup") as s:
                s.set_attribute("redis.hit", True)
                s.set_attribute("cache.key_prefix", f"emb_bucket|{role}")
                time.sleep(lats["cache_lookup"] / 1000)
            req_span.set_attribute("total_ms", sum(lats.values()))
            return

        # Embed
        with tracer.start_as_current_span("bedrock.embed") as s:
            s.set_attribute("model.id", "cohere.embed-multilingual-v3")
            s.set_attribute("input_type", "search_query")
            s.set_attribute("dimensions", 1024)
            time.sleep(lats["embed"] / 1000)

        # Retrieval
        with tracer.start_as_current_span("opensearch.retrieve") as s:
            s.set_attribute("rbac.filter", f"classification IN allowed_levels for {role}")
            s.set_attribute("index", "tax-docs")
            s.set_attribute("hnsw.m", 32)
            s.set_attribute("hnsw.ef", 128)
            with tracer.start_as_current_span("opensearch.hnsw_knn"):
                time.sleep(lats["hnsw"] / 1000)
            with tracer.start_as_current_span("opensearch.bm25"):
                time.sleep(lats["bm25"] / 1000)
            with tracer.start_as_current_span("opensearch.rrf_fusion"):
                s.set_attribute("rrf.k", 60)
                time.sleep(lats["rrf"] / 1000)

        if "redaction" in lats:
            with tracer.start_as_current_span("rbac.redaction_guard") as s:
                s.set_attribute("chunks_dropped", 3)
                s.set_attribute("reason", "classification > user.ceiling")
                time.sleep(lats["redaction"] / 1000)

        # Rerank
        with tracer.start_as_current_span("bedrock.rerank") as s:
            s.set_attribute("model.id", "cohere.rerank-v3-5:0")
            s.set_attribute("top_k_in", 60)
            s.set_attribute("top_k_out", 8)
            time.sleep(lats["rerank"] / 1000)

        # Grade
        with tracer.start_as_current_span("haiku.grade") as s:
            s.set_attribute("model.id", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
            s.set_attribute("verdict", verdict)
            time.sleep(lats["grade"] / 1000)

        if verdict == "Relevant" and "generate" in lats:
            # Generate
            with tracer.start_as_current_span("haiku.generate") as s:
                s.set_attribute("model.id", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
                s.set_attribute("bedrock.input_tokens", 512)
                s.set_attribute("bedrock.output_tokens", 128)
                s.set_attribute("stream", True)
                time.sleep(lats["generate"] / 1000)

            # Verify
            with tracer.start_as_current_span("citation.verify") as s:
                s.set_attribute("depth", "lid+onderdeel+sub")
                s.set_attribute("grounded", True)
                time.sleep(lats["verify"] / 1000)

        # Audit
        with tracer.start_as_current_span("audit.emit") as s:
            s.set_attribute("sink.cloudwatch", True)
            s.set_attribute("sink.s3_object_lock_7yr", True)
            s.set_attribute("user.role", role)
            time.sleep(lats["audit"] / 1000)

        total = sum(lats.values())
        req_span.set_attribute("total_ms", total)
        print(f"  Emitted: [{role}] {q[:50]}... -> {verdict} ({total}ms)")


print("Emitting 5 representative RAG traces to Jaeger...")
for i, scenario in enumerate(SCENARIOS):
    print(f"Trace {i+1}/{len(SCENARIOS)}:")
    emit_trace(scenario)
    time.sleep(0.2)

provider.shutdown()
print("\nDone. Open http://localhost:16686 - Service: tax-rag")
