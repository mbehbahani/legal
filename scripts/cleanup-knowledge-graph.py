"""
cleanup-knowledge-graph.py

Normalizes .understand-anything/knowledge-graph.json in-place:

  1. Flatten non-standard node fields
       label       -> name
       description -> summary  (top-level or inside properties{})
       properties  -> merged into top level, then removed

  2. Remap non-standard edge types to the nearest valid spec type
       references   -> documents
       defines      -> defines_schema
       supports     -> depends_on
       uses         -> depends_on
       referenced_by-> documents   (reversed direction)
       extends      -> inherits

  3. Remove orphan concept nodes
       concept nodes with no filePath AND fewer than 2 edges

  4. Drop edges that became dangling after step 3

  5. Write a clean backup of the original before overwriting

Writes:
  .understand-anything/knowledge-graph.json         (cleaned)
  .understand-anything/knowledge-graph.backup.json  (original)
"""

import json
import shutil
from pathlib import Path
from collections import Counter

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH   = PROJECT_ROOT / ".understand-anything" / "knowledge-graph.json"
BACKUP_PATH  = PROJECT_ROOT / ".understand-anything" / "knowledge-graph.backup.json"

# ── Valid edge types (from the /understand spec) ─────────────────────────────
VALID_EDGE_TYPES = {
    "imports", "exports", "contains", "inherits", "implements",
    "calls", "subscribes", "publishes", "middleware",
    "reads_from", "writes_to", "transforms", "validates",
    "depends_on", "tested_by", "configures",
    "related", "similar_to",
    "deploys", "serves", "provisions", "triggers",
    "migrates", "documents", "routes", "defines_schema",
}

# ── Edge type remapping ───────────────────────────────────────────────────────
EDGE_TYPE_MAP = {
    "references":    "documents",
    "defines":       "defines_schema",
    "supports":      "depends_on",
    "uses":          "depends_on",
    "referenced_by": "documents",   # direction flip handled below
    "extends":       "inherits",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def flatten_node(node: dict) -> dict:
    """Normalise a single node to the canonical schema."""
    n = dict(node)

    # 1a. label -> name
    if "label" in n and "name" not in n:
        n["name"] = n.pop("label")
    elif "label" in n:
        n.pop("label")

    # 1b. top-level description -> summary
    if "description" in n and "summary" not in n:
        n["summary"] = n.pop("description")
    elif "description" in n:
        n.pop("description")

    # 1c. properties{} -> merge useful sub-keys, then delete
    if "properties" in n:
        props = n.pop("properties")
        if isinstance(props, dict):
            # pull description out of properties if summary still missing
            if "summary" not in n and "description" in props:
                n["summary"] = props["description"]
            # preserve any other useful sub-keys not already on the node
            for k, v in props.items():
                if k not in n and k not in ("description",):
                    n[k] = v

    # 1d. guarantee required fields exist
    if "name" not in n or not n["name"]:
        n["name"] = n.get("id", "unknown").split(":")[-1].split("/")[-1]
    if "summary" not in n or not n["summary"]:
        n["summary"] = f'{n["name"]} — {n.get("type", "node")}.'
    if not n.get("tags"):
        n["tags"] = ["untagged"]
    if "complexity" not in n:
        n["complexity"] = "moderate"

    return n


def remap_edge(edge: dict) -> dict:
    """Remap non-standard edge type; flip source/target for referenced_by."""
    e = dict(edge)
    original_type = e.get("type", "")

    if original_type in EDGE_TYPE_MAP:
        new_type = EDGE_TYPE_MAP[original_type]
        # referenced_by is semantically reversed: A referenced_by B  =>  B documents A
        if original_type == "referenced_by":
            e["source"], e["target"] = e["target"], e["source"]
        e["type"] = new_type

    return e


def edge_count(nodes, edges):
    """Return {node_id: degree} for the given edge list."""
    counts: Counter = Counter()
    for e in edges:
        counts[e["source"]] += 1
        counts[e["target"]] += 1
    return counts


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Reading  {GRAPH_PATH}")
    with open(GRAPH_PATH, encoding="utf-8") as f:
        graph = json.load(f)

    # backup
    shutil.copy(GRAPH_PATH, BACKUP_PATH)
    print(f"Backup → {BACKUP_PATH}")

    nodes_in  = graph["nodes"]
    edges_in  = graph["edges"]
    print(f"\nInput : {len(nodes_in)} nodes, {len(edges_in)} edges")

    # ── Step 1: flatten nodes ─────────────────────────────────────────────────
    nodes = [flatten_node(n) for n in nodes_in]
    fixed_fields = sum(
        1 for a, b in zip(nodes_in, nodes) if a != b
    )
    print(f"\nStep 1 — field normalisation")
    print(f"  {fixed_fields} nodes had non-standard fields (label/description/properties)")

    # ── Step 2: remap edge types ──────────────────────────────────────────────
    edges = [remap_edge(e) for e in edges_in]
    remapped = sum(1 for a, b in zip(edges_in, edges) if a.get("type") != b.get("type"))
    leftover  = [e["type"] for e in edges if e["type"] not in VALID_EDGE_TYPES]
    print(f"\nStep 2 — edge type remapping")
    print(f"  {remapped} edges remapped to standard types")
    if leftover:
        print(f"  WARNING: {len(leftover)} edges still have non-standard types: {set(leftover)}")
    else:
        print(f"  All edge types are now in the valid spec set ✓")

    # ── Step 3: remove orphan concept nodes ───────────────────────────────────
    degrees = edge_count(nodes, edges)
    orphans = {
        n["id"] for n in nodes
        if n["type"] == "concept"
        and not n.get("filePath")
        and degrees.get(n["id"], 0) < 2
    }
    nodes = [n for n in nodes if n["id"] not in orphans]
    print(f"\nStep 3 — orphan concept removal")
    print(f"  Removed {len(orphans)} orphan concept nodes: {orphans or '{none}'}")

    # ── Step 4: drop dangling edges ───────────────────────────────────────────
    valid_ids = {n["id"] for n in nodes}
    edges_clean = [
        e for e in edges
        if e.get("source") in valid_ids and e.get("target") in valid_ids
    ]
    dangling = len(edges) - len(edges_clean)
    print(f"\nStep 4 — dangling edge removal")
    print(f"  Dropped {dangling} edges whose source/target was removed")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\nOutput: {len(nodes)} nodes, {len(edges_clean)} edges")

    edge_type_dist = Counter(e["type"] for e in edges_clean)
    print(f"\nEdge type distribution after cleanup:")
    for t, c in sorted(edge_type_dist.items(), key=lambda x: -x[1]):
        marker = "" if t in VALID_EDGE_TYPES else "  ← NON-STANDARD"
        print(f"  {t:25s} {c:3d}{marker}")

    node_type_dist = Counter(n["type"] for n in nodes)
    print(f"\nNode type distribution after cleanup:")
    for t, c in sorted(node_type_dist.items(), key=lambda x: -x[1]):
        print(f"  {t:20s} {c}")

    # ── Write ─────────────────────────────────────────────────────────────────
    graph["nodes"] = nodes
    graph["edges"] = edges_clean
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"\nSaved → {GRAPH_PATH}")


if __name__ == "__main__":
    main()
