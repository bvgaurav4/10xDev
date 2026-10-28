#!/usr/bin/env python3
"""Trace neighbors and similar symbols for candidate nodes, then return the induced subgraph."""
import argparse
import json
from pathlib import Path

from swegemma import graph as sg

DATA_DIR = Path("/kaggle/input/competitions/gemma-4-developer-agent")
GRAPH_DIR = str(DATA_DIR / "graphs")
EMBEDDINGS_DIR = str(DATA_DIR / "embeddings")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Repository, e.g. fastapi/fastapi")
    parser.add_argument("--base-commit", required=True, help="Repository base commit SHA")
    parser.add_argument(
        "--nodes",
        nargs="+",
        required=True,
        help="One or more candidate symbol names to start from",
    )
    parser.add_argument("--max-neighbors", type=int, default=10)
    parser.add_argument("--k", type=int, default=5, help="Number of similar nodes per candidate")
    args = parser.parse_args()

    repo_graph = sg.get_graph(
        repo_name=args.repo,
        graph_dir=GRAPH_DIR,
        embeddings_dir=EMBEDDINGS_DIR,
        base_commit=args.base_commit,
    )

    focal_nodes = []
    for node in args.nodes:
        if node in repo_graph and node not in focal_nodes:
            focal_nodes.append(node)

    neighbors_by_node = {}
    similar_by_node = {}
    for query_node in list(focal_nodes):
        neighbors = sg.get_neighbor(
            node=query_node,
            graph=repo_graph,
            max_neighbors=args.max_neighbors,
        )
        neighbors_by_node[query_node] = list(neighbors)
        for neighbor in neighbors:
            if neighbor in repo_graph and neighbor not in focal_nodes:
                focal_nodes.append(neighbor)

        similar = sg.get_similar_nodes(
            node=query_node,
            repo_name=args.repo,
            k=args.k,
            graph=repo_graph,
            graph_dir=GRAPH_DIR,
            embeddings_dir=EMBEDDINGS_DIR,
            base_commit=args.base_commit,
        )
        similar_by_node[query_node] = [
            {"node_name": item["node_name"], "similarity": item["similarity"]}
            for item in similar
        ]

    subgraph = sg.get_induced_subgraph(repo_graph, focal_nodes)
    print(
        json.dumps(
            {
                "repo": args.repo,
                "base_commit": args.base_commit,
                "requested_nodes": args.nodes,
                "matched_nodes": focal_nodes,
                "neighbors": neighbors_by_node,
                "similar": similar_by_node,
                "subgraph": {
                    "node_count": subgraph.number_of_nodes(),
                    "edge_count": subgraph.number_of_edges(),
                    "nodes": list(subgraph.nodes()),
                    "edges": [list(edge) for edge in subgraph.edges()],
                },
            }
        )
    )


if __name__ == "__main__":
    main()
