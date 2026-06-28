from pydantic import BaseModel, Field


class MSTNode(BaseModel):
    """Un nodo del subgrafo con sus metricas y posicion sugerida para graficar."""

    id: str
    in_degree: int
    is_hub: bool = Field(..., description="True si supera el umbral de influencia")
    size: int = Field(..., description="Tamano sugerido para el frontend")
    x: float
    y: float


class MSTEdge(BaseModel):
    """Una arista no dirigida con su costo; in_mst indica si pertenece al arbol."""

    source: str
    target: str
    weight: float = Field(..., description="Costo = 1 / (popularidad combinada + 1)")
    combined_popularity: int = Field(..., description="in_degree[source] + in_degree[target]")
    in_mst: bool = Field(..., description="True si la arista pertenece al MST")


class MSTStats(BaseModel):
    """Resumen del calculo del arbol de expansion minima."""

    num_nodes: int
    num_edges: int
    mst_num_edges: int
    total_cost: float = Field(..., description="Suma de los costos de las aristas del MST")
    top_n: int


class MSTResponse(BaseModel):
    """Resultado del arbol de expansion minima, listo para que el frontend lo dibuje."""

    nodes: list[MSTNode]
    edges: list[MSTEdge]
    stats: MSTStats
