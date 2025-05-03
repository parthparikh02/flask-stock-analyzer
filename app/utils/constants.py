import enum


class HttpStatusCode(enum.Enum):
    """Enum for storing different http status code."""
    OK = '200'
    CREATED = '201'
    BAD_REQUEST = '400'
    UNAUTHORIZED = '401'
    FORBIDDEN = '403'
    NOT_FOUND = '404'
    INTERNAL_SERVER_ERROR = '500'
    TOO_MANY_REQUESTS = '429'