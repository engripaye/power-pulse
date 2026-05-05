from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, complaints, locations, reports, status

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])

