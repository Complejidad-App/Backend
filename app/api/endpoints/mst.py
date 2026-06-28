from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.schemas.mst import MSTResponse
from app.services.mst_service import compute_minimum_spanning_tree

router = APIRouter(prefix="/mst", tags=["mst"])


@router.get("/kruskal", response_model=MSTResponse)
def kruskal(
    top_n: int = Query(60, ge=2, le=500, description="Cantidad de nodos top por in-degree"),
    threshold: int = Query(14, ge=0, description="Umbral de in-degree para marcar un hub"),
) -> MSTResponse:
    """Arbol de Expansion Minima (Kruskal) sobre la red de seguidores.

    Beneficio para la empresa: identifica el conjunto minimo de conexiones (y por
    ende de creadores) necesario para cubrir toda la red objetivo al menor costo,
    evitando pagar por colaboraciones redundantes.
    """
    try:
        return compute_minimum_spanning_tree(settings.FOLLOWERS_DATASET_PATH, top_n, threshold)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Dataset no encontrado en '{exc}'. Coloca el archivo de edgelist alli "
                "o ajusta FOLLOWERS_DATASET_PATH en el .env."
            ),
        ) from exc
