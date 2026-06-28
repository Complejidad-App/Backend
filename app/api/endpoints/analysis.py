from fastapi import APIRouter

from app.schemas.analysis import NumbersRequest, StatsResponse
from app.services.analysis_service import compute_stats

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/stats", response_model=StatsResponse)
def analyze_numbers(payload: NumbersRequest) -> StatsResponse:
    """Recibe una lista de numeros y devuelve estadisticas + histograma en JSON.

    Es un ejemplo de como exponer el resultado de un algoritmo para que el
    frontend lo consuma y lo grafique.
    """
    return compute_stats(payload.values)
