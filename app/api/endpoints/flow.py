from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.schemas.flow import MaxFlowResponse
from app.services.flow_service import compute_max_flow

router = APIRouter(prefix="/flow", tags=["flow"])


@router.get("/max", response_model=MaxFlowResponse)
def max_flow(
    top_n: int = Query(60, ge=2, le=500, description="Cantidad de nodos top por in-degree"),
    source: str | None = Query(None, description="Nodo origen; por defecto el de mayor in-degree"),
    target: str | None = Query(None, description="Nodo destino; por defecto el siguiente hub"),
) -> MaxFlowResponse:
    """Flujo maximo de audiencia garantizada entre un creador (origen) y un nicho.

    Estima la audiencia máxima garantizada que un creador puede mover hacia un nicho objetivo, permitiendo comparar candidatos y elegir la inversión publicitaria con mejor retorno.
    """
    try:
        return compute_max_flow(settings.FOLLOWERS_DATASET_PATH, top_n, source, target)
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
