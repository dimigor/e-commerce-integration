from shopify_integration.core.exceptions import BaseAuthenticationError


class InvalidAccessTokenError(BaseAuthenticationError):
    message = "Access token you have provided is invalid"


class NotAuthenticatedError(BaseAuthenticationError):
    message = "We are unable to authenticate you"
