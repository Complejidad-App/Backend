from pathlib import Path

import networkx as nx

from app.schemas.flow import FlowEdge, FlowNode, FlowStats, MaxFlowResponse
from app.services.graph_utils import load_graph, top_in_degree_subgraph


def compute_max_flow(
    dataset_path: str | Path,
    top_n: int = 60,
    source: str | None = None,
    target: str | None = None,
) -> MaxFlowResponse:
    """Calcula el flujo maximo entre un creador (origen) y un nicho (destino).

    Adaptacion de `flujo_maximo.py`: en vez de dibujar con matplotlib, devuelve el
    valor del flujo y el subgrafo (nodos + aristas con capacidad/flujo) como JSON.

    Modelo: la capacidad de la arista (u, v) aproxima cuanta audiencia puede fluir
    hacia v, usando `in_degree[v] + 1`. Si no se indican origen/destino, se eligen
    los dos nodos de mayor in-degree (creador mas influyente -> siguiente hub).

    Lanza FileNotFoundError si falta el dataset y ValueError si los nodos son
    invalidos; el endpoint los traduce a 404 / 400.
    """
    graph = load_graph(dataset_path)
    subgraph = top_in_degree_subgraph(graph, top_n)

    in_degrees = dict(subgraph.in_degree())

    # Capacidad de cada arista = in_degree del destino + 1 (evita capacidad 0).
    for u, v in subgraph.edges():
        subgraph[u][v]["capacity"] = in_degrees[v] + 1

    ranked = sorted(in_degrees, key=lambda node: in_degrees[node], reverse=True)

    if source is None:
        source = ranked[0]
    if target is None:
        target = next((node for node in ranked if node != source), None)

    if source not in subgraph:
        raise ValueError(f"El nodo origen '{source}' no esta en el top {top_n} por in-degree.")
    if target not in subgraph:
        raise ValueError(f"El nodo destino '{target}' no esta en el top {top_n} por in-degree.")
    if source == target:
        raise ValueError("El origen y el destino deben ser nodos distintos.")

    flow_value, flow_dict = nx.maximum_flow(subgraph, source, target, capacity="capacity")

    pos = nx.circular_layout(subgraph)

    def role(node: str) -> str:
        if node == source:
            return "origen"
        if node == target:
            return "destino"
        return "otro"

    nodes = [
        FlowNode(
            id=str(node),
            in_degree=in_degrees[node],
            role=role(node),
            size=700 if node in (source, target) else 200,
            x=float(pos[node][0]),
            y=float(pos[node][1]),
        )
        for node in subgraph.nodes()
    ]

    edges = []
    for u, v in subgraph.edges():
        flow = flow_dict.get(u, {}).get(v, 0)
        edges.append(
            FlowEdge(
                source=str(u),
                target=str(v),
                capacity=subgraph[u][v]["capacity"],
                flow=flow,
                is_active=flow > 0,
            )
        )

    stats = FlowStats(
        num_nodes=subgraph.number_of_nodes(),
        num_edges=len(edges),
        num_active_edges=sum(1 for edge in edges if edge.is_active),
        top_n=top_n,
    )

    return MaxFlowResponse(
        source=str(source),
        target=str(target),
        max_flow=flow_value,
        nodes=nodes,
        edges=edges,
        stats=stats,
    )
