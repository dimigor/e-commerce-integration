from typing import Annotated

from fastapi import Depends

from shopify_integration.api.dependancies import get_shop
from shopify_integration.app.domain.shop.models import Shop as _Shop

Shop = Annotated[_Shop, Depends(get_shop)]
