from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from shopify_integration.api.annotations import Shop
from shopify_integration.api.schemas.shipping_info import ShippingInfoCreateSchema, ShippingInfoReadSchema
from shopify_integration.app.annotations import DomainMediator
from shopify_integration.app.domain.shipping_info.commands.get_shipping import (
    GetShippingInfoQuery,
    GetShippingInfoQueryResult,
)
from shopify_integration.app.domain.shipping_info.commands.update_shipping import UpdateShippingInfoCommand

shipping_router = APIRouter(prefix="/shipping")


@shipping_router.get("/", response_model=ShippingInfoReadSchema, status_code=status.HTTP_200_OK)
@cache(expire=10)
async def get_shipping_info(shop: Shop, command_executor: DomainMediator):
    result: GetShippingInfoQueryResult = await command_executor.execute(command=GetShippingInfoQuery(shop=shop))
    return ShippingInfoReadSchema.model_validate(result)


@shipping_router.post("/", status_code=status.HTTP_200_OK)
async def update_shipping_info(shop: Shop, shipping_info: ShippingInfoCreateSchema, command_executor: DomainMediator):
    await command_executor.execute(
        command=UpdateShippingInfoCommand(shop=shop, shipping_info=shipping_info),
    )
