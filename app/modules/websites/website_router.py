from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.exceptions.swagger_examples import NOT_FOUND, VALIDATION_ERROR, BAD_REQUEST, INTERNAL_SERVER_ERROR
from .website_service import WebsiteService
from .schema.create_website_schema import CreateWebsite
from .schema.update_website_schema import UpdateWebsite
from .schema.response_website_schema import ResponseWebsite, ResponseListWebsite, ResponseDetailWebsite

website_router = APIRouter(
    prefix='/websites',
    tags=['Website']
)

def get_website_service(db: Session = Depends(get_db)) -> WebsiteService:
    """Dependency injection untuk WebsiteService"""
    return WebsiteService(db)

@website_router.post('/', response_model=ResponseWebsite, status_code=201)
def create_website(body: CreateWebsite, service: WebsiteService = Depends(get_website_service)):
    website = service.create(body)
    return website

@website_router.get("/", response_model=ResponseListWebsite, status_code=200)
def get_all_websites(service: WebsiteService = Depends(get_website_service)):
    return service.getAll()

@website_router.get("/{id}/trigger", status_code=200)
def trigger_scrapping(id: int, service: WebsiteService = Depends(get_website_service)):
    return service.trigger_scrapping(id)

@website_router.get(
    "/{id}",
    response_model=ResponseDetailWebsite,
    responses={
        404: NOT_FOUND,
        422: VALIDATION_ERROR,
        500: INTERNAL_SERVER_ERROR
    }
)
def get_website(id: int, service: WebsiteService = Depends(get_website_service)):
    return service.getById(id)

@website_router.put("/{id}", response_model=ResponseWebsite)
def update_website(id: int, body: UpdateWebsite, service: WebsiteService = Depends(get_website_service)):
    return service.update(id, body)

@website_router.delete("/{id}", status_code=201)
def delete_website(id: int, service: WebsiteService = Depends(get_website_service)):
    return service.delete(id)