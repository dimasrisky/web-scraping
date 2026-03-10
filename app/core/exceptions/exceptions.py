from typing import Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Detail error individual"""
    code: str = Field(..., description="Error code (e.g., validationError, notFound)")
    detail: str = Field(..., description="Human readable error message")
    attr: Optional[str] = Field(None, description="Field or attribute that caused the error")


class ErrorResponse(BaseModel):
    """Template response untuk semua error"""
    type: str = Field(..., description="Error type (e.g., clientError, serverError)")
    errors: List[ErrorDetail] = Field(default_factory=list, description="List of error details")
    path: Optional[str] = Field(None, description="Request path that caused the error")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the error occurred")


class AppException(Exception):
    """Base exception untuk aplikasi"""

    def __init__(
        self,
        status_code: int,
        error_type: str,
        errors: List[ErrorDetail],
        path: Optional[str] = None
    ):
        self.status_code = status_code
        self.error_type = error_type
        self.errors = errors if isinstance(errors, list) else [errors]
        self.path = path
        super().__init__()


# ============== Client Errors (4xx) ==============

class BadRequestException(AppException):
    """400 Bad Request"""

    def __init__(
        self,
        detail: str,
        code: str = "badRequest",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=400,
            error_type="clientError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class UnauthorizedException(AppException):
    """401 Unauthorized"""

    def __init__(
        self,
        detail: str = "Authentication required",
        code: str = "unauthorized",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=401,
            error_type="clientError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class ForbiddenException(AppException):
    """403 Forbidden"""

    def __init__(
        self,
        detail: str = "You don't have permission to access this resource",
        code: str = "forbidden",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=403,
            error_type="clientError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class NotFoundException(AppException):
    """404 Not Found"""

    def __init__(
        self,
        detail: str = "Resource not found",
        code: str = "notFound",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=404,
            error_type="clientError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class ValidationException(AppException):
    """422 Validation Error"""

    def __init__(
        self,
        errors: List[ErrorDetail],
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=422,
            error_type="clientError",
            errors=errors,
            path=path
        )


class ConflictException(AppException):
    """409 Conflict"""

    def __init__(
        self,
        detail: str,
        code: str = "conflict",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=409,
            error_type="clientError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class RateLimitException(AppException):
    """429 Too Many Requests"""

    def __init__(
        self,
        detail: str = "Too many requests, please try again later",
        code: str = "rateLimitExceeded",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=429,
            error_type="clientError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


# ============== Server Errors (5xx) ==============

class InternalServerException(AppException):
    """500 Internal Server Error"""

    def __init__(
        self,
        detail: str = "Server error occurred.",
        code: str = "internalServerError",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=500,
            error_type="serverError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class BadGatewayException(AppException):
    """502 Bad Gateway"""

    def __init__(
        self,
        detail: str = "Upstream service error",
        code: str = "badGateway",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=502,
            error_type="serverError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )


class ServiceUnavailableException(AppException):
    """503 Service Unavailable"""

    def __init__(
        self,
        detail: str = "Service temporarily unavailable",
        code: str = "serviceUnavailable",
        attr: Optional[str] = None,
        path: Optional[str] = None
    ):
        super().__init__(
            status_code=503,
            error_type="serverError",
            errors=[ErrorDetail(code=code, detail=detail, attr=attr)],
            path=path
        )
