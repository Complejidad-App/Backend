from pydantic import BaseModel, Field


class NumbersRequest(BaseModel):
    """Datos de entrada para un analisis estadistico simple."""

    values: list[float] = Field(..., description="Lista de numeros a analizar", min_length=1)

    model_config = {
        "json_schema_extra": {
            "examples": [{"values": [4, 8, 15, 16, 23, 42]}],
        }
    }


class StatsResponse(BaseModel):
    """Resultado del analisis estadistico, listo para graficar en el frontend."""

    count: int
    mean: float
    median: float
    std: float
    min: float
    max: float
    histogram: list["HistogramBin"]


class HistogramBin(BaseModel):
    """Un intervalo del histograma con su frecuencia."""

    bin_start: float
    bin_end: float
    frequency: int


StatsResponse.model_rebuild()
