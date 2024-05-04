from fastapi import APIRouter

from shopify_integration.api.annotations import Shop
from shopify_integration.api.schemas.shipment import ShipmentLabelReadSchema, ShipmentsFilterSchema
from shopify_integration.app.annotations import DomainMediator
from shopify_integration.app.domain.order.commands.get_orders import GetOrdersResult, GetOrdersQuery
from shopify_integration.app.domain.order.filters import OrderFilterSet
from shopify_integration.app.domain.order.schemas.status import OrderStatus
from shopify_integration.app.domain.shipment.commands.create_shipment import CreateShipmentCommand
from shopify_integration.app.domain.shipment.commands.get_shipment import GetShipmentQuery, GetShipmentResult
from shopify_integration.app.domain.shipment.commands.get_shipments import GetShipmentsQuery, GetShipmentsResult
from shopify_integration.app.domain.shipment.filters import ShipmentFilterSet

shipments_router = APIRouter(prefix="/shipments")


@shipments_router.post("/")
async def create_shipments(shop: Shop, shipments_filter: ShipmentsFilterSchema, command_executor: DomainMediator):
    filters = OrderFilterSet(shop_id__eq=shop.id, id__in=shipments_filter.ids)
    if not filters.id__in:
        filters.status__eq = OrderStatus.NEW

    orders_result: GetOrdersResult = await command_executor.execute(
        command=GetOrdersQuery(
            orders_filter=filters
        )
    )
    for order in orders_result.orders:
        await command_executor.execute(
            command=CreateShipmentCommand(shop=shop, order=order),
        )


@shipments_router.get("/labels/{tracking_number}", response_model=ShipmentLabelReadSchema)
async def get_shipment_label(shop: Shop, tracking_number: str, command_executor: DomainMediator):
    filters = ShipmentFilterSet(shop_id__eq=shop.id, tracking_number__eq=tracking_number)
    result: GetShipmentResult = await command_executor.execute(command=GetShipmentQuery(shipment_filter=filters))
    return ShipmentLabelReadSchema.model_validate(result.shipment.model_dump())


@shipments_router.get("/labels/", response_model=list[ShipmentLabelReadSchema])
async def get_shipments_labels(shop: Shop, tracking_numbers: list[str], command_executor: DomainMediator):
    filters = ShipmentFilterSet(shop_id__eq=shop.id, tracking_number__in=tracking_numbers)
    result: GetShipmentsResult = await command_executor.execute(command=GetShipmentsQuery(shipment_filter=filters))
    return [ShipmentLabelReadSchema.model_validate(shipment.model_dump()) for shipment in result.shipments]
