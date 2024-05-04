from jose import JWTError, jwt

from shopify_integration.api.exceptions import InvalidAccessTokenError
from shopify_integration.api.schemas.jwt import JWTPayload
from shopify_integration.infra.config import config

_JWT_ALGORITHM = config.JWT_ALGORITHMS
_SECRET_KEY = config.JWT_SECRET


def encode_jwt(payload: JWTPayload, algorithm: str = _JWT_ALGORITHM) -> str:
    """
    Encode JWT payload with secret key and algorithm.

    :param payload: JWT payload
    :param algorithm: JWT algorithm
    :return: JWT token
    """
    to_encode = payload.model_dump()

    return jwt.encode(to_encode, _SECRET_KEY, algorithm=algorithm)


def decode_jwt(
    token: str,
    algorithms: str | list[str] = _JWT_ALGORITHM,
    key: str = _SECRET_KEY,
) -> JWTPayload:
    """
    Decode JWT token with key and algorithm.

    :param token: JWT token
    :param algorithms: JWT algorithms
    :param key: JWT secret key
    :return: JWT payload

    :raises InvalidAccessTokenError: if token is invalid
    """
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, key, algorithms=algorithms)
        if not payload:
            raise InvalidAccessTokenError()
    except JWTError:
        raise InvalidAccessTokenError()

    return JWTPayload(**payload)
