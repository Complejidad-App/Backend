from fastapi import APIRouter

from app.api.endpoints import analysis, flow, graph, greedy, health, mst

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(analysis.router)
api_router.include_router(graph.router)
api_router.include_router(flow.router)
api_router.include_router(mst.router)
api_router.include_router(greedy.router)
