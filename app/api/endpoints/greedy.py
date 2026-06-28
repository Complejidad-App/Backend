from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.schemas.greedy import InfluenceMaxResponse
from app.services.greedy_service import maximize_influence

router = APIRouter(prefix="/greedy", tags=["greedy"])


@router.get("/influence-maximization", response_model=InfluenceMaxResponse)
def influence_maximization(
    k: int = Query(5, ge=1, le=500, description="Presupuesto: cantidad de creadores a contratar"),
    top_n: int = Query(60, ge=1, le=500, description="Cantidad de nodos top por in-degree"),
) -> InfluenceMaxResponse:
    """Maximizacion de Influencia con algoritmo voraz (Greedy).

    Beneficio para la empresa: con un presupuesto de k creadores, recomienda el
    conjunto que maximiza el alcance total y muestra los retornos decrecientes,
    justificando cuantos creadores conviene contratar antes de dejar de invertir.
    """
    try:
        return maximize_influence(settings.FOLLOWERS_DATASET_PATH, top_n, k)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Dataset no encontrado en '{exc}'. Coloca el archivo de edgelist alli "
                "o ajusta FOLLOWERS_DATASET_PATH en el .env."
            ),
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
