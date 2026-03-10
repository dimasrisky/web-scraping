from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1 import v1
from app.core.config import config
from app.core.exceptions.exceptions import AppException
from app.core.exceptions.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title=config.PROJECT_NAME,
    summary=config.SUMMARY,
    version=config.VERSION
)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(v1)

@app.get('/')
def root():
    return { "message": "This is root api" }