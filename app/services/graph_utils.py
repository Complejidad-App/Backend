from pathlib import Path

import networkx as nx


def load_graph(dataset_path: str | Path) -> nx.DiGraph:
    """Lee un edgelist como grafo dirigido. Lanza FileNotFoundError si no existe."""
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(str(path))
    return nx.read_edgelist(path, create_using=nx.DiGraph())


def top_in_degree_subgraph(graph: nx.DiGraph, top_n: int) -> nx.DiGraph:
    """Devuelve el subgrafo con los `top_n` nodos de mayor in-degree."""
    top_nodes = sorted(graph.in_degree, key=lambda item: item[1], reverse=True)[:top_n]
    return graph.subgraph([node for node, _ in top_nodes]).copy()
