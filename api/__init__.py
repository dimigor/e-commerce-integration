from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import ValidationException
from fastapi.routing import APIRoute
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from shopify_integration.api.router import api_router
from shopify_integration.core.exceptions import BaseError
from shopify_integration.infra.config import config
from shopify_integration.infra.error_handlers import handle_app_error, handle_validation_error
from shopify_integration.infra.redis.cache_key_builder import cache_key_builder
from shopify_integration.infra.redis.constants import REDIS_API_CACHE_PREFIX, REDIS_API_RATE_LIMIT_PREFIX
from shopify_integration.infra.redis.redis import get_redis
from shopify_integration.platforms.shopify.api.router import shopify_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = get_redis()
    sentry_sdk.init(dsn=config.SENTRY_DSN, traces_sample_rate=1.0, send_default_pii=True, enable_tracing=True)
    FastAPICache.init(backend=RedisBackend(redis), prefix=REDIS_API_CACHE_PREFIX, key_builder=cache_key_builder)
    await FastAPILimiter.init(redis=redis, prefix=REDIS_API_RATE_LIMIT_PREFIX)
    yield
    await FastAPILimiter.close()
    FastAPICache.reset()


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


class ShopifyIntegration(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.mount("/static", StaticFiles(directory="shopify_integration/static"), name="ui")
        self.include_middlewares()
        self.include_api_routers()
        self.include_exception_handlers()

    def include_api_routers(self):
        self.include_router(api_router)
        self.include_router(shopify_router)

    def include_middlewares(self):
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost", "http://localhost:5173", "https://localhost", "https://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def include_exception_handlers(self):
        self.add_exception_handler(BaseError, handle_app_error)
        self.add_exception_handler(ValidationError, handle_validation_error)
        self.add_exception_handler(ValidationException, handle_validation_error)


app = ShopifyIntegration(
    lifespan=lifespan, openapi_url="/api/v1/openapi.json", generate_unique_id_function=custom_generate_unique_id
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
