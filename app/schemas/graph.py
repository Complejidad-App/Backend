from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    """Un nodo del grafo con sus metricas y una posicion sugerida para graficar."""

    id: str
    in_degree: int = Field(..., description="Numero de seguidores dentro del subgrafo")
    out_degree: int = Field(..., description="Numero de seguidos dentro del subgrafo")
    is_hub: bool = Field(..., description="True si supera el umbral de influencia")
    category: str = Field(..., description="'creador' (hub) o 'usuario'")
    size: int = Field(..., description="Tamano sugerido del nodo para el frontend")
    x: float = Field(..., description="Coordenada X sugerida (circular layout)")
    y: float = Field(..., description="Coordenada Y sugerida (circular layout)")


class GraphEdge(BaseModel):
    """Una arista dirigida: source sigue a target."""

    source: str
    target: str


class GraphStats(BaseModel):
    """Resumen del subgrafo analizado."""

    num_nodes: int
    num_edges: int
    threshold: int
    top_n: int


class GraphAnalysisResponse(BaseModel):
    """Resultado del analisis de grafo, listo para que el frontend lo dibuje."""

    nodes: list[GraphNode]
    edges: list[GraphEdge]
    stats: GraphStats
