#!/usr/bin/env python3
"""List the nodes in a repository's precomputed code graph."""
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
    args = parser.parse_args()

    repo_graph = sg.get_graph(
        repo_name=args.repo,
        graph_dir=GRAPH_DIR,
        embeddings_dir=EMBEDDINGS_DIR,
        base_commit=args.base_commit,
    )

    nodes = list(repo_graph.nodes())
    print(
        json.dumps(
            {
                "repo": args.repo,
                "base_commit": args.base_commit,
                "node_count": repo_graph.number_of_nodes(),
                "edge_count": repo_graph.number_of_edges(),
                "nodes": nodes,
            }
        )
    )


if __name__ == "__main__":
    main()
