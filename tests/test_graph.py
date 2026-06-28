from pathlib import Path

from app.services.graph_service import analyze_followers_graph

SAMPLE = Path(__file__).parent / "data" / "sample_edgelist.txt"


def test_analyze_followers_graph_structure():
    result = analyze_followers_graph(SAMPLE, top_n=10, threshold=3)

    assert result.stats.num_nodes == len(result.nodes)
    assert result.stats.threshold == 3
    assert result.stats.top_n == 10

    # El nodo "1" recibe 4 seguidores en el sample -> debe ser hub con umbral 3.
    node_1 = next(n for n in result.nodes if n.id == "1")
    assert node_1.in_degree == 4
    assert node_1.is_hub is True
    assert node_1.category == "creador"

    # Solo aristas que tocan algun hub.
    hub_ids = {n.id for n in result.nodes if n.is_hub}
    assert all(e.source in hub_ids or e.target in hub_ids for e in result.edges)


def test_analyze_followers_graph_top_n_limits_nodes():
    result = analyze_followers_graph(SAMPLE, top_n=3, threshold=3)
    assert result.stats.num_nodes == 3


def test_analyze_followers_graph_missing_file():
    try:
        analyze_followers_graph("data/no_existe.txt")
    except FileNotFoundError:
        return
    raise AssertionError("Se esperaba FileNotFoundError")
