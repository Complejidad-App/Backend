from collections import deque
from pathlib import Path

import networkx as nx

from app.schemas.greedy import GreedyNode, GreedyStats, GreedyStep, InfluenceMaxResponse
from app.services.graph_utils import load_graph, top_in_degree_subgraph


def _reachable(graph: nx.DiGraph, start: str) -> set[str]:
    """Conjunto de nodos alcanzables desde `start` (BFS por aristas dirigidas)."""
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph.successors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def maximize_influence(
    dataset_path: str | Path,
    top_n: int = 60,
    k: int = 5,
) -> InfluenceMaxResponse:
    """Maximizacion de influencia con un algoritmo voraz (Kempe et al., 2003).

    Adaptacion de `algoritmo_voraz.py`: en cada uno de los `k` pasos elige al
    creador que aporta mas audiencia nueva (cobertura marginal via BFS), sin
    reconsiderar elecciones previas. Devuelve la seleccion, la curva de cobertura
    y el subgrafo como JSON en vez de dibujar con matplotlib.

    Lanza FileNotFoundError si falta el dataset y ValueError si `k` es invalido;
    el endpoint los traduce a 404 / 400.
    """
    if k < 1:
        raise ValueError("El presupuesto k debe ser al menos 1.")

    graph = load_graph(dataset_path)
    subgraph = top_in_degree_subgraph(graph, top_n)

    in_degrees = dict(subgraph.in_degree())
    candidates = list(subgraph.nodes())

    # No tiene sentido contratar mas creadores que nodos disponibles.
    effective_k = min(k, len(candidates))

    selected: list[str] = []
    covered: set[str] = set()
    steps: list[GreedyStep] = []

    for step in range(effective_k):
        best_node = None
        best_gain = -1
        best_new_reach: set[str] = set()

        for node in candidates:
            if node in selected:
                continue
            new_reach = _reachable(subgraph, node) - covered
            gain = len(new_reach)
            if gain > best_gain:
                best_gain = gain
                best_node = node
                best_new_reach = new_reach

        if best_node is None:
            break

        selected.append(best_node)
        covered |= best_new_reach
        steps.append(
            GreedyStep(
                step=step + 1,
                node=str(best_node),
                marginal_gain=best_gain,
                cumulative_coverage=len(covered),
            )
        )

    pos = nx.circular_layout(subgraph)

    def status(node: str) -> str:
        if node in selected:
            return "seleccionado"
        if node in covered:
            return "cubierto"
        return "no_cubierto"

    nodes = [
        GreedyNode(
            id=str(node),
            in_degree=in_degrees[node],
            status=status(node),
            size=700 if node in selected else (200 if node in covered else 150),
            x=float(pos[node][0]),
            y=float(pos[node][1]),
        )
        for node in subgraph.nodes()
    ]

    num_nodes = subgraph.number_of_nodes()
    coverage_pct = round(len(covered) / num_nodes * 100, 2) if num_nodes else 0.0

    stats = GreedyStats(
        num_nodes=num_nodes,
        top_n=top_n,
        k=effective_k,
        total_covered=len(covered),
        coverage_pct=coverage_pct,
    )

    return InfluenceMaxResponse(
        selected=[str(node) for node in selected],
        steps=steps,
        nodes=nodes,
        stats=stats,
    )
