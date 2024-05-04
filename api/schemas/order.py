from datetime import datetime

from fastapi import Query
from pydantic import AliasChoices, AliasPath, Field

from shopify_integration.api.schemas.shipment import ShipmentReadSchema
from shopify_integration.app.domain.order.schemas.status import OrderStatus
from shopify_integration.core.base_models import BaseAPIReadModel, BaseFrozenModel


class OrderReadSchema(BaseAPIReadModel):
    id: str
    external_id: int
    status: OrderStatus
    payment_status: str
    fulfillment_status: str
    placed_at: datetime
    order_reference: str = Field(
        validation_alias=AliasChoices(AliasPath("shipment_details", "order_reference"), "orderReference")
    )
    recipient_country: str = Field(
        validation_alias=AliasChoices(AliasPath("shipment_details", "to_address", "country"), "destinationCountry")
    )
    recipient_name: str = Field(
        validation_alias=AliasChoices(AliasPath("shipment_details", "to_address", "name"), "receiverName")
    )
    shipment: ShipmentReadSchema | None


class OrdersPaginated(BaseAPIReadModel):
    total_count: int
    orders: OrderReadSchema


class OrdersFilterSchema(BaseFrozenModel):
    status: OrderStatus = Query(...)
