from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from shopify_integration.infra.config import config


def get_jwt_expire_time(
    expire_in_seconds: int = config.JWT_ACCESS_TOKEN_EXPIRES,
) -> datetime:
    return datetime.utcnow() + timedelta(seconds=expire_in_seconds)


class JWTPayload(BaseModel):
    id: int
    exp: datetime = Field(default_factory=get_jwt_expire_time)
