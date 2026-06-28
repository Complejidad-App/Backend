from pathlib import Path

import networkx as nx

from app.schemas.mst import MSTEdge, MSTNode, MSTResponse, MSTStats
from app.services.graph_utils import load_graph, top_in_degree_subgraph


def compute_minimum_spanning_tree(
    dataset_path: str | Path,
    top_n: int = 60,
    threshold: int = 14,
) -> MSTResponse:
    """Calcula el arbol de expansion minima (Kruskal) sobre el subgrafo top-N.

    Adaptacion de `mst.py`: en vez de dibujar con matplotlib, devuelve los nodos,
    todas las aristas (marcando cuales pertenecen al MST con `in_mst`) y el costo
    total como JSON, para que el frontend resalte el set minimo de conexiones.

    Costo de la arista (u, v) = 1 / (in_degree[u] + in_degree[v] + 1): cuanto mas
    populares son ambos extremos, mas barata es la conexion. Lanza FileNotFoundError
    si falta el dataset; el endpoint lo traduce a 404.
    """
    graph = load_graph(dataset_path)
    subgraph = top_in_degree_subgraph(graph, top_n)

    in_degrees = dict(subgraph.in_degree())

    # Kruskal/Prim trabajan sobre grafos no dirigidos.
    undirected = subgraph.to_undirected()
    for u, v in undirected.edges():
        combined = in_degrees[u] + in_degrees[v]
        undirected[u][v]["weight"] = 1 / (combined + 1)

    mst = nx.minimum_spanning_tree(undirected, weight="weight", algorithm="kruskal")
    mst_edge_set = {frozenset((u, v)) for u, v in mst.edges()}

    pos = nx.circular_layout(subgraph)

    nodes = [
        MSTNode(
            id=str(node),
            in_degree=in_degrees[node],
            is_hub=in_degrees[node] >= threshold,
            size=400 if in_degrees[node] >= threshold else 150,
            x=float(pos[node][0]),
            y=float(pos[node][1]),
        )
        for node in subgraph.nodes()
    ]

    edges = []
    for u, v, data in undirected.edges(data=True):
        edges.append(
            MSTEdge(
                source=str(u),
                target=str(v),
                weight=data["weight"],
                combined_popularity=in_degrees[u] + in_degrees[v],
                in_mst=frozenset((u, v)) in mst_edge_set,
            )
        )

    total_cost = sum(data["weight"] for _, _, data in mst.edges(data=True))

    stats = MSTStats(
        num_nodes=subgraph.number_of_nodes(),
        num_edges=undirected.number_of_edges(),
        mst_num_edges=mst.number_of_edges(),
        total_cost=total_cost,
        top_n=top_n,
    )

    return MSTResponse(nodes=nodes, edges=edges, stats=stats)
