from pathlib import Path

import pytest

from app.services.mst_service import compute_minimum_spanning_tree

SAMPLE = Path(__file__).parent / "data" / "sample_edgelist.txt"


def test_mst_structure_and_cost():
    result = compute_minimum_spanning_tree(SAMPLE, top_n=10, threshold=3)

    assert result.stats.num_nodes == len(result.nodes)
    assert result.stats.mst_num_edges == sum(1 for e in result.edges if e.in_mst)

    # Un MST sobre un grafo conexo de N nodos tiene N-1 aristas como maximo.
    assert result.stats.mst_num_edges <= result.stats.num_nodes - 1

    # total_cost es la suma de los pesos de las aristas marcadas in_mst.
    cost_from_edges = sum(e.weight for e in result.edges if e.in_mst)
    assert result.stats.total_cost == pytest.approx(cost_from_edges)


def test_mst_weight_and_popularity_consistency():
    result = compute_minimum_spanning_tree(SAMPLE, top_n=10, threshold=3)
    for edge in result.edges:
        assert edge.weight == pytest.approx(1 / (edge.combined_popularity + 1))


def test_mst_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        compute_minimum_spanning_tree("data/no_existe.txt")
