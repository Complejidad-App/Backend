from pathlib import Path

import networkx as nx

from app.schemas.graph import GraphAnalysisResponse, GraphEdge, GraphNode, GraphStats
from app.services.graph_utils import load_graph, top_in_degree_subgraph


def analyze_followers_graph(
    dataset_path: str | Path,
    top_n: int = 60,
    threshold: int = 14,
) -> GraphAnalysisResponse:
    """Analiza un grafo de seguidores y devuelve nodos, aristas y estadisticas en JSON.

    Adaptacion del script original `grafos.py`: en lugar de dibujar con matplotlib,
    calcula las metricas (in-degree, hubs, layout) y las devuelve como datos para
    que el frontend renderice el grafo. Asi se trabajan los algoritmos en este API:
    el algoritmo vive en `services/`, su salida se modela en `schemas/` y se expone
    en `api/endpoints/`.

    Lanza FileNotFoundError si el dataset no existe; el endpoint lo traduce a 404.
    """
    graph = load_graph(dataset_path)
    subgraph = top_in_degree_subgraph(graph, top_n)

    in_degrees = dict(subgraph.in_degree())
    out_degrees = dict(subgraph.out_degree())
    hubs = {node for node in subgraph.nodes() if in_degrees[node] >= threshold}

    pos = nx.circular_layout(subgraph)

    nodes = [
        GraphNode(
            id=str(node),
            in_degree=in_degrees[node],
            out_degree=out_degrees[node],
            is_hub=node in hubs,
            category="creador" if node in hubs else "usuario",
            size=400 if node in hubs else 200,
            x=float(pos[node][0]),
            y=float(pos[node][1]),
        )
        for node in subgraph.nodes()
    ]

    edges = [
        GraphEdge(source=str(u), target=str(v))
        for u, v in subgraph.edges()
        if u in hubs or v in hubs
    ]

    stats = GraphStats(
        num_nodes=subgraph.number_of_nodes(),
        num_edges=len(edges),
        threshold=threshold,
        top_n=top_n,
    )

    return GraphAnalysisResponse(nodes=nodes, edges=edges, stats=stats)
