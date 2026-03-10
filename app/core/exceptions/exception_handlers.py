from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .exceptions import AppException, ErrorResponse, ErrorDetail


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handler untuk custom AppException"""
    response = ErrorResponse(
        type=exc.error_type,
        errors=exc.errors,
        path=f"{request.method} {request.url.path}",
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json")
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handler untuk bawaan HTTPException FastAPI/Starlette"""
    # Mapping status code ke error type
    error_type = "clientError" if exc.status_code < 500 else "serverError"

    # Mapping status code ke error code
    error_codes = {
        400: "badRequest",
        401: "unauthorized",
        403: "forbidden",
        404: "notFound",
        422: "validationError",
        429: "rateLimitExceeded",
        500: "internalServerError",
        502: "badGateway",
        503: "serviceUnavailable",
    }

    code = error_codes.get(exc.status_code, "httpError")

    response = ErrorResponse(
        type=error_type,
        errors=[ErrorDetail(code=code, detail=exc.detail)],
        path=f"{request.method} {request.url.path}",
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json")
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler untuk validation error (Pydantic)"""
    errors = []
    for error in exc.errors():
        # Ambil field name dari error location
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append(
            ErrorDetail(
                code="validationError",
                detail=error["msg"],
                attr=field
            )
        )

    response = ErrorResponse(
        type="clientError",
        errors=errors,
        path=f"{request.method} {request.url.path}",
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump(mode="json")
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler untuk exception yang tidak ter-handle (fallback)"""
    # Di production, jangan expose raw error message ke client
    error_detail = str(exc) if not getattr(exc, "__class__") else "An unexpected error occurred"

    response = ErrorResponse(
        type="serverError",
        errors=[ErrorDetail(code="internalServerError", detail=error_detail)],
        path=f"{request.method} {request.url.path}",
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json")
    )
