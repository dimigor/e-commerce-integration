from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from shopify_integration.api.annotations import Shop
from shopify_integration.api.schemas.order import OrderReadSchema, OrdersFilterSchema
from shopify_integration.app.annotations import DomainMediator
from shopify_integration.app.domain.order.commands.get_orders import GetOrdersQuery, GetOrdersResult
from shopify_integration.app.domain.order.filters import OrderFilterSet

orders_router = APIRouter(prefix="/orders")


@orders_router.get("/", response_model=list[OrderReadSchema])
@cache(expire=60)
async def get_orders(shop: Shop, command_executor: DomainMediator, orders_filter: OrdersFilterSchema = Depends()):
    result: GetOrdersResult = await command_executor.execute(
        command=GetOrdersQuery(
            orders_filter=OrderFilterSet(shop_id__eq=shop.id, status__eq=orders_filter.status),
        )
    )
    return result.orders
