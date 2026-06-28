from pathlib import Path

import networkx as nx

from app.schemas.graph import GraphAnalysisResponse, GraphEdge, GraphNode, GraphStats


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
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    graph = nx.read_edgelist(path, create_using=nx.DiGraph())

    top_nodes = sorted(graph.in_degree, key=lambda item: item[1], reverse=True)[:top_n]
    subgraph = graph.subgraph([node for node, _ in top_nodes]).copy()

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
