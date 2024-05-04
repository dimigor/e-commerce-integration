from shopify_integration.app.domain.shipping_info.defs import CarrierOptions
from shopify_integration.app.domain.shipping_info.schemas.update import ShippingInfoBase, ShippingInfoUpdate


class ShippingInfoCreateSchema(ShippingInfoUpdate):
    carrier: CarrierOptions = CarrierOptions.YODEL


class ShippingInfoReadSchema(ShippingInfoBase):
    ...
