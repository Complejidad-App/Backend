from pathlib import Path

import pytest

from app.services.greedy_service import maximize_influence

SAMPLE = Path(__file__).parent / "data" / "sample_edgelist.txt"


def test_greedy_selection_and_steps():
    result = maximize_influence(SAMPLE, top_n=10, k=3)

    assert len(result.selected) == result.stats.k
    assert [s.node for s in result.steps] == result.selected

    # La cobertura acumulada es monotona no decreciente (submodularidad).
    coverages = [s.cumulative_coverage for s in result.steps]
    assert coverages == sorted(coverages)
    assert result.steps[-1].cumulative_coverage == result.stats.total_covered

    # Los nodos seleccionados aparecen con status 'seleccionado'.
    selected_status = {n.id: n.status for n in result.nodes if n.id in result.selected}
    assert all(status == "seleccionado" for status in selected_status.values())


def test_greedy_k_capped_to_node_count():
    result = maximize_influence(SAMPLE, top_n=3, k=99)
    # No se pueden contratar mas creadores que nodos disponibles.
    assert result.stats.k == 3
    assert len(result.selected) == 3


def test_greedy_invalid_k_raises():
    with pytest.raises(ValueError):
        maximize_influence(SAMPLE, top_n=10, k=0)


def test_greedy_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        maximize_influence("data/no_existe.txt")
