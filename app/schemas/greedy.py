from pydantic import BaseModel, Field


class GreedyStep(BaseModel):
    """Un paso del algoritmo voraz: el creador elegido y la cobertura ganada."""

    step: int = Field(..., description="Numero de paso (1-indexado)")
    node: str = Field(..., description="Creador seleccionado en este paso")
    marginal_gain: int = Field(..., description="Usuarios nuevos alcanzados en este paso")
    cumulative_coverage: int = Field(..., description="Audiencia total cubierta tras este paso")


class GreedyNode(BaseModel):
    """Un nodo del subgrafo con su estado respecto a la seleccion voraz."""

    id: str
    in_degree: int
    status: str = Field(..., description="'seleccionado', 'cubierto' o 'no_cubierto'")
    size: int = Field(..., description="Tamano sugerido para el frontend")
    x: float
    y: float


class GreedyStats(BaseModel):
    """Resumen de la maximizacion de influencia."""

    num_nodes: int
    top_n: int
    k: int = Field(..., description="Presupuesto: creadores contratados")
    total_covered: int
    coverage_pct: float = Field(..., description="Porcentaje de la red cubierto")


class InfluenceMaxResponse(BaseModel):
    """Resultado de la maximizacion de influencia, listo para graficar."""

    selected: list[str] = Field(..., description="Creadores recomendados, en orden")
    steps: list[GreedyStep]
    nodes: list[GreedyNode]
    stats: GreedyStats
