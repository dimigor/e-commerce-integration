from shopify_integration.app.domain.shipment.schemas.status import ShipmentStatus
from shopify_integration.core.base_models import BaseAPIReadModel, BaseFrozenModel


class ShipmentReadSchema(BaseAPIReadModel):
    tracking_number: str | None
    error_message: str | None
    status: ShipmentStatus


class ShipmentLabelReadSchema(BaseAPIReadModel):
    label: str


class ShipmentsFilterSchema(BaseFrozenModel):
    ids: list[int] | None
