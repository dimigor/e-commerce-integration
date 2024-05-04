from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from shopify_integration.api.auth.jwt import decode_jwt
from shopify_integration.api.exceptions import NotAuthenticatedError
from shopify_integration.api.schemas.jwt import JWTPayload
from shopify_integration.app.annotations import DomainMediator
from shopify_integration.app.domain.shop.models import Shop
from shopify_integration.app.domain.shop.queries.get_shop import GetShopByIdQuery
from shopify_integration.app.repositories.exceptions import DoesNotExistError

api_key_scheme = APIKeyHeader(name="Authorization")


def decode_jwt_auth_header(access_token: str = Depends(api_key_scheme)) -> JWTPayload:
    return decode_jwt(access_token)


async def get_shop(
    jwt_data: Annotated[JWTPayload, Depends(decode_jwt_auth_header)],
    domain_mediator: DomainMediator,
) -> Shop:
    """Gets shop instance by given shop_id"""
    try:
        result = await domain_mediator.execute(
            command=GetShopByIdQuery(shop_id=jwt_data.id),
        )
    except DoesNotExistError:
        raise NotAuthenticatedError()
    return result.shop
