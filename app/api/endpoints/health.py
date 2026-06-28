from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de verificacion para saber si la API esta viva."""
    return {"status": "ok"}
