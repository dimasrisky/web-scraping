# Web Scraping API

A robust and flexible web scraping API built with FastAPI that allows you to create, manage, and trigger web scraping operations for various news websites.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Parser Configuration](#parser-configuration)
- [Data Flow](#data-flow)
- [Error Handling](#error-handling)
- [Development](#development)

## Features

- **RESTful API** - Complete CRUD operations for website management
- **Flexible Parser Configuration** - JSON-based parsers for different website structures
- **Headless Browser Support** - Uses DynamicFetcher for JavaScript-rendered pages
- **Database Management** - PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Asynchronous Task Queue** - Celery with Redis/RabbitMQ for background scraping
- **Standardized Error Handling** - Custom exception system with detailed error responses
- **Swagger Documentation** - Auto-generated API documentation with examples

## Tech Stack

### Core Framework
| Technology | Version | Description |
|------------|---------|-------------|
| FastAPI | 0.135.1 | Modern, fast web framework for building APIs |
| Pydantic | 2.12.5 | Data validation using Python type annotations |
| Uvicorn | 0.41.0 | ASGI server for FastAPI applications |

### Database
| Technology | Version | Description |
|------------|---------|-------------|
| SQLAlchemy | 2.0.48 | SQL toolkit and ORM |
| Alembic | 1.18.4 | Database migration tool |
| PostgreSQL | - | Database system (via psycopg2-binary) |

### Task Queue
| Technology | Version | Description |
|------------|---------|-------------|
| Celery | 5.6.2 | Distributed task queue |
| Redis/RabbitMQ | - | Message broker for Celery |

### Web Scraping
| Technology | Version | Description |
|------------|---------|-------------|
| Scrapling | 0.4.1 | Web scraping library |
| Playwright | 1.56.0 | Browser automation |
| PatchRight | 1.56.0 | Enhanced Playwright |
| LXML | 6.0.2 | XML and HTML parsing |

### Utilities
- **Loguru** - Advanced logging
- **python-dotenv** - Environment variable management
- **orjson** - Fast JSON processing

## Project Structure

```
web-scraping/
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── api/
│   │   └── v1.py                   # API router with v1 prefix
│   ├── core/
│   │   ├── config.py               # Application configuration
│   │   ├── database.py             # Database connection & session management
│   │   └── exceptions/             # Custom exception handling
│   │       ├── exceptions.py       # Base exception classes
│   │       ├── exception_handlers.py  # Exception handlers
│   │       └── swagger_examples.py     # Error response examples
│   └── modules/
│       ├── queue/                  # Celery task queue module
│       │   ├── celery.py           # Celery app configuration
│       │   └── task.py             # Scraping tasks
│       └── websites/               # Website scraping module
│           ├── website_router.py   # API endpoints
│           ├── website_service.py  # Business logic
│           ├── model/
│           │   └── website_model.py    # SQLAlchemy model
│           └── schema/             # Pydantic schemas
├── alembic/                        # Database migrations
│   └── versions/
├── parser.json                     # Parser config examples
├── requirements.txt                # Python dependencies
├── alembic.ini                     # Alembic configuration
├── .env.example                    # Environment variables template
└── ERROR_DOCS.md                   # Exception handler documentation
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis or RabbitMQ (for Celery task queue)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd web-scraping
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start Redis/RabbitMQ** (if using Celery queue)
   ```bash
   # For Redis (macOS with Homebrew)
   brew services start redis

   # For RabbitMQ (macOS with Homebrew)
   brew services start rabbitmq
   ```

6. **Start the Celery worker** (in a separate terminal)
   ```bash
   celery -A app.modules.queue.celery:celery_app worker --loglevel=info
   ```

7. **Start the FastAPI application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Configuration

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=fast_api_scraping

# Celery Configuration (for task queue)
CELERY_BROKER=redis://localhost:6379/0
# Or for RabbitMQ:
# CELERY_BROKER=amqp://guest:guest@localhost:5672//

CELERY_BACKEND=redis://localhost:6379/0
# Or for RabbitMQ:
# CELERY_BACKEND=rpc://
```

## API Endpoints

Base URL: `http://localhost:8000/api/v1`

### Website Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/websites` | Create a new website configuration |
| GET | `/websites` | Get all websites |
| GET | `/websites/{id}` | Get website by ID |
| PUT | `/websites/{id}` | Update website configuration |
| DELETE | `/websites/{id}` | Delete website |

### Scraping Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/websites/{id}/trigger` | Trigger synchronous scraping process |
| GET | `/websites/trigger/queue/{id}` | Trigger asynchronous scraping (Celery queue) |

### Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage

### Create Website Configuration

```bash
POST /api/v1/websites
Content-Type: application/json

{
  "name": "Example News",
  "url": "https://example.com/news",
  "parser": {
    "waitSelectorList": ".news-list",
    "waitSelectorDetail": ".article-content",
    "list": [...],
    "detail": [...]
  },
  "isActive": true
}
```

### Get All Websites

```bash
GET /api/v1/websites
```

### Trigger Synchronous Scraping

```bash
GET /api/v1/websites/1/trigger
```

**Response:**
```json
[
  {
    "title": "Article Title",
    "creationDate": "2026-03-10",
    "content": "<p>Article content...</p>",
    "imageUrl": "https://example.com/image.jpg",
    "thumbnailUrl": "https://example.com/thumb.jpg"
  }
]
```

### Trigger Asynchronous Scraping (Queue)

```bash
GET /api/v1/websites/trigger/queue/1
```

**Response:**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "queued",
  "message": "Scraping task has been queued successfully"
}
```

**Note:** Make sure the Celery worker is running before triggering queue tasks.

## Parser Configuration

The parser configuration uses JSON to define how to extract data from websites. Each parser consists of:

### Structure

```json
{
  "waitSelectorList": "selector-to-wait-for-list",
  "waitSelectorDetail": "selector-to-wait-for-detail",
  "list": [
    {
      "name": "urls",
      "selectors": [
        {
          "selector": "a.article-link",
          "action": "attrs",
          "attr": "href"
        },
        {
          "action": "add_firsts",
          "add": "https://example.com"
        }
      ]
    }
  ],
  "detail": [
    {
      "name": "title",
      "selectors": [
        {
          "selector": "h1.article-title",
          "action": "text"
        }
      ]
    },
    {
      "name": "content",
      "selectors": [
        {
          "selector": ".article-content",
          "action": "html"
        }
      ]
    },
    {
      "name": "imageUrl",
      "selectors": [
        {
          "selector": ".article-image img",
          "action": "attr",
          "attr": "src"
        }
      ]
    },
    {
      "name": "creationDate",
      "selectors": [
        {
          "action": "dateTimeNow"
        }
      ]
    }
  ]
}
```

### Parser Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `text` | Extract inner text | - |
| `html` | Extract inner HTML | - |
| `attr` | Extract attribute | `attr`: attribute name |
| `attrs` | Extract array of attributes | `attr`: attribute name |
| `add_first` | Prefix single value | `add`: prefix string |
| `add_firsts` | Prefix array values | `add`: prefix string |
| `dateTimeNow` | Set to current date | - |

## Data Flow

### Synchronous Scraping

```
┌─────────┐    ┌─────────────┐    ┌────────────────┐    ┌──────────┐
│ Client  │───▶│ FastAPI     │───▶│ WebsiteService │───▶│ Database │
│ Request │    │ Router      │    │                │    │          │
└─────────┘    └─────────────┘    └────────────────┘    └──────────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ DynamicFetcher │
                                  │ (Headless)     │
                                  └────────────────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ Parse & Return │
                                  │ Structured Data│
                                  └────────────────┘
```

### Asynchronous Scraping (Queue)

```
┌─────────┐    ┌─────────────┐    ┌────────────────┐    ┌──────────┐
│ Client  │───▶│ FastAPI     │───▶│   Celery Task  │───▶│  Redis/  │
│ Request │    │ Router      │    │    (Queued)    │    │ RabbitMQ │
└─────────┘    └─────────────┘    └────────────────┘    └──────────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ Celery Worker  │
                                  │ (Background)   │
                                  └────────────────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ DynamicFetcher │
                                  │ (Headless)     │
                                  └────────────────┘
```

### Scraping Process

1. **Request** - API receives trigger request with website ID
2. **Fetch Configuration** - Retrieve website parser config from database
3. **Fetch List Page** - Use DynamicFetcher to load the list page
4. **Extract URLs** - Parse list page to get article URLs
5. **Fetch Detail Pages** - Load each article URL
6. **Extract Content** - Parse detail pages for structured data
7. **Return Response** - Send JSON array of scraped articles (or task ID for queue)

## Development

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Monitoring Celery Tasks

```bash
# View active tasks
celery -A app.modules.queue.celery:celery_app inspect active

# View registered tasks
celery -A app.modules.queue.celery:celery_app inspect registered

# View worker statistics
celery -A app.modules.queue.celery:celery_app inspect stats
```

### Flower (Celery Monitoring UI)

Optional: Install Flower for real-time monitoring of Celery tasks:

```bash
pip install flower

# Start Flower
celery -A app.modules.queue.celery:celery_app flower

# Access Flower UI
# http://localhost:5555
```
