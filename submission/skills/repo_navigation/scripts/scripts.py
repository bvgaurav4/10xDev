# will have all the scripts needed for searching and debugging
import json 
from swegemma import graph as sg
import glob
import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

def search_repo(repo):
    DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
    WORKING_DIR = Path('/kaggle/working')
    WORKING_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_DIR = str(DATA_DIR / 'graphs')
    EMBEDDINGS_DIR = str(DATA_DIR / 'embeddings')

    # Load the pre-computed repository code graph and node embeddings for the sample task
    repo_graph = sg.get_graph(
        repo_name=repo.repo,
        graph_dir=GRAPH_DIR,
        embeddings_dir=EMBEDDINGS_DIR,
        base_commit=repo.base_commit,
    )
    sample_nodes = list(repo_graph.nodes())
    print(f'Graph for {repo.repo} ({repo.instance_id}):')
    print(f'  Nodes: {repo_graph.number_of_nodes()}, Edges: {repo_graph.number_of_edges()}')

    # Select a connected symbol and query structural neighbors (callers, callees, definitions)
    query_node = next((n for n, deg in repo_graph.degree() if deg >= 5), sample_nodes[0])
    neighbors = sg.get_neighbor(
        node=query_node,
        graph=repo_graph,
        max_neighbors=10,
    )
    print(f'\nNeighbors of {query_node!r} (showing up to 5):')
    for n in neighbors[:5]:
        print(f'  - {n}')

    # Search for semantically similar code nodes using pre-computed vector embeddings
    similar = sg.get_similar_nodes(
        node=query_node,
        repo_name=repo.repo,
        k=5,
        graph=repo_graph,
        graph_dir=GRAPH_DIR,
        embeddings_dir=EMBEDDINGS_DIR,
        base_commit=repo.base_commit,
    )
    print(f'\nTop similar nodes to {query_node!r}:')
    for item in similar:
        print(f"  - {item['node_name']} (similarity={item['similarity']:.4f})")

    # Extract an induced subgraph connecting the query symbol and its neighbors
    focal_nodes = [query_node, *neighbors[:4]]
    subgraph = sg.get_induced_subgraph(repo_graph, focal_nodes)
    print(
        f'\nInduced subgraph over {len(focal_nodes)} focal nodes: '
        f'{subgraph.number_of_nodes()} nodes, {subgraph.number_of_edges()} edges'
    )

def custom_script_execution(script):
    namespace = {
        "json":json,
        "sg":sg,
        "glob":glob,
        "importlib":importlib,
        "shutil":shutil,
        "os":os,
        "Path":Path}
    exec(script,namespace,namespace)

def testing_changes(script):
    namespace = {
        "json":json,
        "sg":sg,
        "glob":glob,
        "importlib":importlib,
        "shutil":shutil,
        "os":os,
        "Path":Path}
    exec(script,namespace,namespace)