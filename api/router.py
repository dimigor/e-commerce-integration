from fastapi.routing import APIRouter

from shopify_integration.api.routes.order import orders_router
from shopify_integration.api.routes.shipment import shipments_router
from shopify_integration.api.routes.shipping_info import shipping_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(orders_router, tags=["orders"])
api_router.include_router(shipping_router, tags=["shipping"])
api_router.include_router(shipments_router, tags=["shipments"])
