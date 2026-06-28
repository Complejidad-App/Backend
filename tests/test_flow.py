from pathlib import Path

import pytest

from app.services.flow_service import compute_max_flow

SAMPLE = Path(__file__).parent / "data" / "sample_edgelist.txt"


def test_compute_max_flow_auto_source_target():
    result = compute_max_flow(SAMPLE, top_n=10)

    # Origen y destino son los dos nodos de mayor in-degree (1 y 2 en el sample).
    assert {result.source, result.target} == {"1", "2"}
    assert result.source != result.target
    assert result.max_flow >= 0

    roles = {n.id: n.role for n in result.nodes}
    assert roles[result.source] == "origen"
    assert roles[result.target] == "destino"

    # num_active_edges coincide con las aristas con flujo > 0.
    assert result.stats.num_active_edges == sum(1 for e in result.edges if e.is_active)
    assert all(e.capacity >= 1 for e in result.edges)


def test_compute_max_flow_explicit_nodes():
    result = compute_max_flow(SAMPLE, top_n=10, source="3", target="1")
    assert result.source == "3"
    assert result.target == "1"


def test_compute_max_flow_same_source_target_raises():
    with pytest.raises(ValueError):
        compute_max_flow(SAMPLE, top_n=10, source="1", target="1")


def test_compute_max_flow_unknown_node_raises():
    with pytest.raises(ValueError):
        compute_max_flow(SAMPLE, top_n=10, source="9999")


def test_compute_max_flow_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        compute_max_flow("data/no_existe.txt")
