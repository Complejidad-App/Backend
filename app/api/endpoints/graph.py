from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.schemas.graph import GraphAnalysisResponse
from app.services.graph_service import analyze_followers_graph

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/followers", response_model=GraphAnalysisResponse)
def followers_graph(
    top_n: int = Query(60, ge=1, le=500, description="Cantidad de nodos top por in-degree"),
    threshold: int = Query(14, ge=0, description="Umbral de in-degree para considerar un hub"),
) -> GraphAnalysisResponse:
    """Analisis del grafo de seguidores (top-N por influencia) en formato JSON.

    Lee el edgelist configurado en `FOLLOWERS_DATASET_PATH` y devuelve los nodos
    con sus metricas, las aristas relevantes y un resumen, para que el frontend
    dibuje la red.
    """
    try:
        return analyze_followers_graph(settings.FOLLOWERS_DATASET_PATH, top_n, threshold)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Dataset no encontrado en '{exc}'. Coloca el archivo de edgelist alli "
                "o ajusta FOLLOWERS_DATASET_PATH en el .env."
            ),
        ) from exc
