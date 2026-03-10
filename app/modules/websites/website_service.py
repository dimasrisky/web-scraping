from sqlalchemy.orm import Session
from typing import List, Optional
from .model.website_model import WebsiteModel
from .schema.create_website_schema import CreateWebsite
from .schema.update_website_schema import UpdateWebsite
from .schema.response_website_schema import ResponseListWebsite, ResponseDetailWebsite, ResponseWebsite
from app.core.exceptions.exceptions import NotFoundException
from scrapling import DynamicFetcher
from fastapi import HTTPException
from datetime import date
from loguru import logger

class WebsiteService:
    def __init__(self, db: Session):
        self.db = db

    def getAll(self) -> ResponseListWebsite:
        """Get all websites"""
        websites = self.db.query(WebsiteModel).all()
        return {
            "data": websites
        }

    def getById(self, id: int) -> ResponseDetailWebsite:
        """Get website by ID"""
        website = self.db.query(WebsiteModel).filter(WebsiteModel.id == id).first()

        if not website:
            raise NotFoundException(detail="Website Not Found", attr="id")
        
        return {
            "data": website
        }
    
    def trigger_scrapping(self, id: int):
        logger.info(f"Starting scraping process for website ID: {id}")

        logger.info(f"Retrieving website configuration from database")
        website = self.db.query(WebsiteModel).filter(WebsiteModel.id == id).first()

        if not website:
            logger.error(f"Website with ID {id} not found in database")
            raise HTTPException(status_code=404, detail=f"Website with ID {id} not found")

        logger.info(f"Website found: {website.name}")
        logger.info(f"Parsing website configuration and parser settings")

        website_dict = ResponseWebsite.model_validate(website).model_dump()

        parser = website_dict["parser"]
        url = website_dict["url"]
        
        logger.info(f"Target URL: {url}")
        logger.info(f"Parser configuration loaded with {len(parser.get('list', []))} list parsers and {len(parser.get('detail', []))} detail parsers")

        logger.info(f"Fetching main page using DynamicFetcher (headless mode)")
        
        try:
            page = DynamicFetcher.fetch(url=url, headless=True, network_idle=True, load_dom=True, wait_selector=parser["waitSelectorList"])
            logger.success(f"Successfully fetched main page: {url}")
        except Exception as e:
            logger.error(f"Failed to fetch main page: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch page: {str(e)}")

        articles = []

        logger.info(f"Starting list parsing - extracting URLs from main page")
        for parser_list in parser["list"]:
            list_name = parser_list["name"]
            logger.info(f"Processing list parser: {list_name}")
            parser[list_name] = []

            for idx, selector in enumerate(parser_list["selectors"]):
                logger.debug(f"  Selector {idx + 1}/{len(parser_list['selectors'])}: {selector}")

                if 'selector' in selector:
                    parser[list_name] = page.css(selector["selector"])
                    print('ini hasilnya')
                    print(page.css(selector["selector"]))
                    logger.debug(f"    Applied CSS selector: {selector['selector']}")

                if 'action' in selector:
                    action = selector["action"]
                    logger.debug(f"    Applying action: {action}")

                    if action == 'attrs':
                        parser[list_name] = parser[list_name].css(f"::attr({selector['attr']})").getall()
                        logger.debug(f"    Extracted attribute '{selector['attr']}', found {len(parser[list_name])} items")

                    if action == 'add_firsts':
                        original_count = len(parser[list_name])
                        for i in range(len(parser[list_name])):
                            parser[list_name][i] = f"{selector['add']}{parser[list_name][i]}"
                        logger.debug(f"    Prefixed {original_count} items with: {selector['add']}")

        logger.info(f"Validating extracted URLs")
        if 'urls' not in parser:
            error_msg = "Parser configuration must include 'urls' field"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)

        urls_count = len(parser["urls"])
        logger.info(f"Found {urls_count} URLs to process")

        if urls_count == 0:
            logger.warning("No URLs found to process. Check parser configuration.")

        logger.info(f"Starting detail page scraping for each URL")
        for idx, url in enumerate(parser["urls"], 1):
            logger.info(f"  Processing URL {idx}/{urls_count}: {url}")

            article = {}

            logger.debug(f"    Fetching detail page...")
            try:
                detail_page = DynamicFetcher.fetch(url, headless=True, network_idle=True, load_dom=True, wait_selector=parser["waitSelectorDetail"])
                logger.debug(f"    Successfully fetched detail page")
            except Exception as e:
                logger.error(f"    Failed to fetch detail page {url}: {str(e)}")
                continue

            logger.debug(f"    Parsing detail fields...")
            for parser_detail in parser["detail"]:
                field_name = parser_detail["name"]
                article[field_name] = ''

                logger.debug(f"      Processing field: {field_name}")

                for selector in parser_detail["selectors"]:
                    if 'selector' in selector:
                        article[field_name] = detail_page.css(selector["selector"])
                        logger.debug(f"        Applied CSS selector: {selector['selector']}")

                    if 'action' in selector:
                        action = selector["action"]
                        logger.debug(f"        Applying action: {action}")

                        if action == 'text':
                            article[field_name] = article[field_name].css("::text").get()
                            logger.debug(f"          Extracted text content")

                        if action == 'attr':
                            article[field_name] = article[field_name].css(f"::attr({selector['attr']})").get()
                            logger.debug(f"          Extracted attribute '{selector['attr']}'")

                        if action == 'add_first':
                            article[field_name] = f"{selector['add']}{article[field_name]}"
                            logger.debug(f"          Prefixed with: {selector['add']}")

                        if action == 'dateTimeNow':
                            article[field_name] = date.today()
                            logger.debug(f"          Set to current date: {date.today()}")

                        if action == 'html':
                            article[field_name] = article[field_name].getall()
                            logger.debug(f"          Extracted HTML content")
                            
            articles.append(article)
            logger.debug(f"    Article {idx} completed with {len(article)} fields")

        logger.success(f"Scraping completed successfully. Total articles scraped: {len(articles)}")
        logger.info(f"Scraping process finished for website ID: {id}")

        return articles

    def create(self, website_data: CreateWebsite) -> WebsiteModel:
        """Create new website"""
        # Convert Pydantic v2 model to dict
        website_dict = website_data.model_dump()

        # Mapping field names (camelCase -> snake_case)
        new_website = WebsiteModel(
            name=website_dict['name'],
            url=website_dict['url'],
            parser=website_dict['parser'],
            is_active=website_dict.get('isActive', True)
        )

        self.db.add(new_website)
        self.db.commit()
        self.db.refresh(new_website)
        return new_website

    def update(self, id: int, website_data: UpdateWebsite) -> Optional[WebsiteModel]:
        """Update website"""
        website = self.db.query(WebsiteModel).filter(WebsiteModel.id == id).first()
        website_dict = website_data.model_dump(exclude_unset=True)
        if website_dict:
            for key, value in website_dict.items():
                setattr(website, key, value)
            self.db.commit()
            self.db.refresh(website)
        return website

    def delete(self, id: int) -> bool:
        """Delete website"""
        website = self.db.query(WebsiteModel).filter(WebsiteModel.id == id).first()
        if website:
            self.db.delete(website)
            self.db.commit()
            return True
        return False
