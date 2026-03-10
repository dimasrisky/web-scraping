"""Pre-defined error response examples untuk Swagger/OpenAPI"""
from typing import Dict, Any

# Base response example template
ERROR_EXAMPLE = {
    "type": "clientError",
    "errors": [
        {
            "code": "notFound",
            "detail": "Resource not found",
            "attr": "id"
        }
    ],
    "path": "GET /api/example/999",
    "timestamp": "2025-03-10T10:00:00.000Z"
}

# Pre-defined error responses
BAD_REQUEST = {
    "description": "Bad Request - Invalid input data",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "badRequest",
                        "detail": "Invalid request data",
                        "attr": "field_name"
                    }
                ],
                "path": "POST /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

UNAUTHORIZED = {
    "description": "Unauthorized - Authentication required",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "unauthorized",
                        "detail": "Authentication required"
                    }
                ],
                "path": "GET /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

FORBIDDEN = {
    "description": "Forbidden - Insufficient permissions",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "forbidden",
                        "detail": "You don't have permission to access this resource"
                    }
                ],
                "path": "GET /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

NOT_FOUND = {
    "description": "Not Found - Resource does not exist",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "notFound",
                        "detail": "Resource not found",
                        "attr": "id"
                    }
                ],
                "path": "GET /api/example/999",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

VALIDATION_ERROR = {
    "description": "Validation Error - Request validation failed",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "validationError",
                        "detail": "Field is required",
                        "attr": "email"
                    }
                ],
                "path": "POST /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

CONFLICT = {
    "description": "Conflict - Resource already exists",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "conflict",
                        "detail": "Resource already exists",
                        "attr": "email"
                    }
                ],
                "path": "POST /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

RATE_LIMIT = {
    "description": "Too Many Requests - Rate limit exceeded",
    "content": {
        "application/json": {
            "example": {
                "type": "clientError",
                "errors": [
                    {
                        "code": "rateLimitExceeded",
                        "detail": "Too many requests, please try again later"
                    }
                ],
                "path": "GET /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

INTERNAL_SERVER_ERROR = {
    "description": "Internal Server Error - Something went wrong",
    "content": {
        "application/json": {
            "example": {
                "type": "serverError",
                "errors": [
                    {
                        "code": "internalServerError",
                        "detail": "Server error occurred"
                    }
                ],
                "path": "GET /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

BAD_GATEWAY = {
    "description": "Bad Gateway - Upstream service error",
    "content": {
        "application/json": {
            "example": {
                "type": "serverError",
                "errors": [
                    {
                        "code": "badGateway",
                        "detail": "Upstream service error"
                    }
                ],
                "path": "GET /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}

SERVICE_UNAVAILABLE = {
    "description": "Service Unavailable - Service temporarily unavailable",
    "content": {
        "application/json": {
            "example": {
                "type": "serverError",
                "errors": [
                    {
                        "code": "serviceUnavailable",
                        "detail": "Service temporarily unavailable"
                    }
                ],
                "path": "GET /api/example",
                "timestamp": "2025-03-10T10:00:00.000Z"
            }
        }
    }
}
