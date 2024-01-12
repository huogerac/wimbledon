from ninja import NinjaAPI

# from ninja.security import django_auth

from ..base.views import router as base_router
from ..core.views import router as core_router

api = NinjaAPI(
    csrf=False,
    title="🏆 Wimbledon API",
    description="Gestão de campeonato mata-mata",
)

api.add_router("/", base_router, tags=["base"])
api.add_router("/core/", core_router, tags=["core"])
