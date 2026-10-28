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


def custom_script_execution(script):
    """
    Execute arbitrary Python code dynamically within a predefined namespace.

    This function allows the agent to execute custom Python scripts for
    flexible computation, repository analysis, and filesystem operations.
    The execution namespace provides access to selected modules and utilities,
    including json, sg, glob, importlib, shutil, os, and Path.

    The script can perform computations, define variables and functions,
    inspect files, and store its final output in the `result` variable.

    Args:
        script (str): A string containing valid Python code to execute.

    Returns:
        Any: The value assigned to `result` by the executed script,
             or None if no result is assigned.

    Raises:
        Exception: Propagates exceptions raised during script execution.

    Note:
        The execution environment is not a secure sandbox. Arbitrary code
        may access or modify resources permitted by the current process.
        Apply appropriate isolation and security controls when executing
        untrusted or agent-generated scripts.
    """
    namespace = {
        "json": json,
        "sg": sg,
        "glob": glob,
        "importlib": importlib,
        "shutil": shutil,
        "os": os,
        "Path": Path,
        "result": None,
    }

    exec(script, namespace, namespace)
    return namespace["result"]


# def testing_changes(script):
#     namespace = {
#         "json":json,
#         "sg":sg,
#         "glob":glob,
#         "importlib":importlib,
#         "shutil":shutil,
#         "os":os,
#         "Path":Path}
#     exec(script,namespace,namespace)

def get_repo_nodes(repo):
    """
        Load the repository's code graph using its name and base commit,
        print graph statistics, and return its nodes.
    """
    DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
    WORKING_DIR = Path('/kaggle/working')
    WORKING_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_DIR = str(DATA_DIR / 'graphs')
    EMBEDDINGS_DIR = str(DATA_DIR / 'embeddings')

    repo_graph = sg.get_graph(
        repo_name=repo.repo,
        graph_dir=GRAPH_DIR,
        embeddings_dir=EMBEDDINGS_DIR,
        base_commit=repo.base_commit,
    )
    sample_nodes = list(repo_graph.nodes())
    print(f'Graph for {repo.repo} ({repo.instance_id}):')
    print(f'  Nodes: {repo_graph.number_of_nodes()}, Edges: {repo_graph.number_of_edges()}')
    return repo_graph.nodes()


def search_repo(repo, candidate_nodes):
    """
    Search a repository's code graph using multiple candidate nodes.
    Collect structural neighbors and semantically similar symbols, then
    return the nodes and edges of the induced subgraph.
    """
    DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
    GRAPH_DIR = str(DATA_DIR / 'graphs')
    EMBEDDINGS_DIR = str(DATA_DIR / 'embeddings')

    repo_graph = sg.get_graph(
        repo_name=repo.repo,
        graph_dir=GRAPH_DIR,
        embeddings_dir=EMBEDDINGS_DIR,
        base_commit=repo.base_commit,
    )

    print(f'Graph for {repo.repo} ({repo.instance_id}):')
    print(f'  Nodes: {repo_graph.number_of_nodes()}, Edges: {repo_graph.number_of_edges()}')

    # Keep only candidates that exist in the graph.
    focal_nodes = []
    for node in candidate_nodes:
        if node in repo_graph and node not in focal_nodes:
            focal_nodes.append(node)

    # Collect structural neighbors and similar nodes for each candidate.
    for query_node in list(focal_nodes):
        neighbors = sg.get_neighbor(
            node=query_node,
            graph=repo_graph,
            max_neighbors=10,
        )

        print(f'\nNeighbors of {query_node!r}:')
        for neighbor in neighbors[:5]:
            print(f'  - {neighbor}')
            if neighbor in repo_graph and neighbor not in focal_nodes:
                focal_nodes.append(neighbor)

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

    # Build the induced subgraph from candidates and their structural neighbors.
    subgraph = sg.get_induced_subgraph(repo_graph, focal_nodes)
    print(
        f'\nInduced subgraph: {subgraph.number_of_nodes()} nodes, '
        f'{subgraph.number_of_edges()} edges'
    )
    return list(subgraph.nodes()), list(subgraph.edges())
