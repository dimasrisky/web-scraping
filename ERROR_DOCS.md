# Exception Handler Documentation

Dokumentasi penggunaan custom exception handler di aplikasi ini.

## Daftar Isi

- [Response Format](#response-format)
- [Daftar Exception](#daftar-exception)
- [Cara Penggunaan](#cara-penggunaan)
- [Contoh Implementasi](#contoh-implementasi)

---

## Response Format

Semua error response memiliki format standar:

```json
{
  "type": "clientError | serverError",
  "errors": [
    {
      "code": "error_code",
      "detail": "Human readable error message",
      "attr": "field_name (optional)"
    }
  ],
  "path": "GET /api/v1/resource",
  "timestamp": "2026-03-10T02:53:00.384Z"
}
```

### Field Penjelasan

| Field | Tipe | Deskripsi |
|-------|------|-----------|
| `type` | string | `clientError` (4xx) atau `serverError` (5xx) |
| `errors` | array | List detail error, bisa multiple untuk validation |
| `errors[].code` | string | Kode error unik |
| `errors[].detail` | string | Pesan error yang bisa dibaca manusia |
| `errors[].attr` | string? | Field/atribut yang menyebabkan error (opsional) |
| `path` | string | HTTP method + path request |
| `timestamp` | string | Waktu terjadinya error (ISO 8601) |

---

## Daftar Exception

### Client Errors (4xx)

| Exception | Status | Code | Kegunaan |
|-----------|--------|------|----------|
| `BadRequestException` | 400 | `badRequest` | Request tidak valid |
| `UnauthorizedException` | 401 | `unauthorized` | Butuh autentikasi |
| `ForbiddenException` | 403 | `forbidden` | Tidak punya akses |
| `NotFoundException` | 404 | `notFound` | Resource tidak ditemukan |
| `ValidationException` | 422 | `validationError` | Validasi data (multiple error) |
| `ConflictException` | 409 | `conflict` | Konflik data |
| `RateLimitException` | 429 | `rateLimitExceeded` | Terlalu banyak request |

### Server Errors (5xx)

| Exception | Status | Code | Kegunaan |
|-----------|--------|------|----------|
| `InternalServerException` | 500 | `internalServerError` | Error tak terduga |
| `BadGatewayException` | 502 | `badGateway` | Error upstream service |
| `ServiceUnavailableException` | 503 | `serviceUnavailable` | Service sedang down |

---

## Cara Penggunaan

### 1. Import Exception

```python
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    InternalServerException,
    ValidationException,
    ErrorDetail
)
```

### 2. Single Error (Sebagian besar exception)

```python
# NotFoundException
if not user:
    raise NotFoundException(
        detail="User not found",
        attr="id"  # optional
    )

# BadRequestException
if not email:
    raise BadRequestException(
        detail="Email is required",
        attr="email"
    )

# InternalServerException
try:
    external_service.call()
except Exception as e:
    raise InternalServerException(
        detail=f"Failed to call external service: {str(e)}"
    )
```

### 3. Multiple Errors (ValidationException)

Untuk error validasi yang membutuhkan multiple error sekaligus:

```python
from app.core.exceptions import ValidationException, ErrorDetail

errors = []

# Validasi name
if not name:
    errors.append(ErrorDetail(
        code="required",
        detail="Name is required",
        attr="name"
    ))

# Validasi email
if not email:
    errors.append(ErrorDetail(
        code="required",
        detail="Email is required",
        attr="email"
    ))
elif "@" not in email:
    errors.append(ErrorDetail(
        code="invalidFormat",
        detail="Invalid email format",
        attr="email"
    ))

# Validasi url
if len(url) > 500:
    errors.append(ErrorDetail(
        code="tooLong",
        detail="URL must be less than 500 characters",
        attr="url"
    ))

# Raise jika ada error
if errors:
    raise ValidationException(errors=errors)
```

### 4. Custom Error Code

```python
raise BadRequestException(
    code="invalidParserConfig",  # custom code
    detail="Parser must contain 'urls' field",
    attr="parser"
)
```

---

## Contoh Implementasi

### Contoh 1: Service Layer

```python
from app.core.exceptions import NotFoundException, InternalServerException

class WebsiteService:
    def get_by_id(self, id: int):
        website = self.db.query(WebsiteModel).filter(WebsiteModel.id == id).first()

        if not website:
            raise NotFoundException(
                detail=f"Website with ID {id} not found",
                attr="id"
            )

        return website

    def scrape(self, id: int):
        try:
            result = fetcher.fetch(url)
            return result
        except ConnectionError as e:
            raise InternalServerException(
                detail=f"Failed to connect: {str(e)}",
                attr="network"
            )
```

### Contoh 2: Router Layer

```python
from fastapi import Request
from app.core.exceptions import NotFoundException, ForbiddenException

@website_router.get("/{id}")
def get_website(id: int, request: Request):
    website = service.get_by_id(id)

    # Cek ownership
    if website.user_id != request.user.id:
        raise ForbiddenException(
            detail="You don't have permission to access this website"
        )

    return website
```

### Contoh 3: Response yang Dihasilkan

**Single Error:**
```json
{
  "type": "clientError",
  "errors": [
    {
      "code": "notFound",
      "detail": "Website with ID 1010 not found",
      "attr": "id"
    }
  ],
  "path": "GET /api/v1/websites/1010/scrape",
  "timestamp": "2026-03-10T02:53:00.384Z"
}
```

**Multiple Errors:**
```json
{
  "type": "clientError",
  "errors": [
    {
      "code": "required",
      "detail": "Name is required",
      "attr": "name"
    },
    {
      "code": "invalidFormat",
      "detail": "Invalid email format",
      "attr": "email"
    }
  ],
  "path": "POST /api/v1/websites",
  "timestamp": "2026-03-10T02:53:00.384Z"
}
```

**Server Error:**
```json
{
  "type": "serverError",
  "errors": [
    {
      "code": "internalServerError",
      "detail": "Failed to fetch page: timeout",
      "attr": ""
    }
  ],
  "path": "GET /api/v1/websites/1/scrape",
  "timestamp": "2026-03-10T02:53:00.384Z"
}
```

---

## Auto-Handled Exceptions

Exception berikut otomatis di-handle oleh framework:

1. **Pydantic Validation Error** → Otomatis dikonversi ke format `ValidationException`
2. **FastAPI HTTPException** → Otomatis dikonversi ke format error standard
3. **Generic Exception** → Ditangkap sebagai `InternalServerException` (500)
