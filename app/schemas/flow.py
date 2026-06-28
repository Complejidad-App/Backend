from pydantic import BaseModel, Field


class FlowNode(BaseModel):
    """Un nodo del subgrafo con su rol en el calculo de flujo maximo."""

    id: str
    in_degree: int
    role: str = Field(..., description="'origen', 'destino' u 'otro'")
    size: int = Field(..., description="Tamano sugerido para el frontend")
    x: float
    y: float


class FlowEdge(BaseModel):
    """Una arista con su capacidad y el flujo que transporta en la solucion."""

    source: str
    target: str
    capacity: int = Field(..., description="Capacidad asignada (in_degree del destino + 1)")
    flow: int = Field(..., description="Flujo que circula por la arista en la solucion optima")
    is_active: bool = Field(..., description="True si la arista lleva flujo > 0 (ruta usada)")


class FlowStats(BaseModel):
    """Resumen del calculo de flujo maximo."""

    num_nodes: int
    num_edges: int
    num_active_edges: int
    top_n: int


class MaxFlowResponse(BaseModel):
    """Resultado del flujo maximo entre origen y destino, listo para graficar."""

    source: str = Field(..., description="Nodo origen (creador / anunciante)")
    target: str = Field(..., description="Nodo destino (nicho objetivo)")
    max_flow: int = Field(..., description="Audiencia maxima garantizada (valor del flujo)")
    nodes: list[FlowNode]
    edges: list[FlowEdge]
    stats: FlowStats
