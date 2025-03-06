from typing import Optional, List
import asyncio
from decorators.retry_on_failure import retry_on_failure
from repositories.repository import Repository
from notifications.notification_strategy import NotificationStrategy
from scrappers.scrapper_strategy import ScrapperStrategy
from scrappers.scrapping_tool import ScrappingTool
from utils.logger import logger
from models.product_model import Product

class WebScrapper:
    def __init__(self, base_url: str, repository: Repository, notification: NotificationStrategy, scrapper: ScrapperStrategy, scrapping_tool: ScrappingTool, max_allowed_page: int = 100):
        self.base_url = base_url
        self.repository = repository
        self.notification = notification
        self.scrapper = scrapper
        self.scrapping_tool = scrapping_tool
        self.MAX_PAGE = max_allowed_page

    @retry_on_failure(retries=5)
    async def get_html(self, url: str, proxy: Optional[str] = None, *args, **kwargs) -> str:
        logger.info(f"Getting HTML from {url}, using proxy: {proxy}")
        try:
            html = await self.scrapping_tool.get_html(url, proxy)
            logger.debug(f"Successfully retrieved HTML from {url}")
            return html
        except Exception as e:
            logger.error(f"Failed to get HTML from {url}: {str(e)}")
            raise

    async def scrape_pages(self, urls: List[str], proxy: Optional[str]) -> List[Product]:
        tasks = [self.get_html(url, proxy) for url in urls]
        logger.info(f"Created tasks for URLs: {urls}")
        try:
            html_pages = await asyncio.gather(*tasks)
            logger.debug("Successfully gathered HTML pages")
            parse_tasks = [self.scrapper.parse_page(html) for html in html_pages]
            scraped_products = await asyncio.gather(*parse_tasks)
            scraped_products = [product for sublist in scraped_products for product in sublist]
            logger.info(f"Scraped {scraped_products} products")
            logger.debug("Successfully parsed HTML pages")
            return scraped_products
        except Exception as e:
            logger.error(f"Failed to scrape pages: {str(e)}")
            raise

    def validate_pages(self, from_page: int, to_page: int):
        logger.debug(f"Validating pages from {from_page} to {to_page}")
        if from_page < 1:
            logger.error("from_page must be positive.")
            raise ValueError("from_page must be positive.")
        if to_page < from_page:
            logger.error("to_page must be greater than or equal to from_page.")
            raise ValueError("to_page must be greater than or equal to from_page.")
        if to_page - from_page > self.MAX_PAGE:
            logger.error(f"max pages to extract at a time must be less than or equal to {self.MAX_PAGE}.")
            raise ValueError(f"max pages to extract at a time must be less than or equal to {self.MAX_PAGE}.")
        logger.debug("Page validation successful")

    async def scrape(self, proxy: Optional[str], pages: Optional[int], to_page: Optional[int], from_page: Optional[int] = 1) -> dict:
        try:
            logger.info(f"Starting scrape from page {from_page} to {to_page} with proxy {proxy}")
            if pages:
                to_page = from_page + pages - 1
            self.validate_pages(from_page, to_page)
            urls = [self.base_url.format(page) for page in range(from_page, to_page + 1)]
            logger.debug(f"Generated URLs: {urls}")
            scrapped_products = await self.scrape_pages(urls, proxy)
            updated_count = self.repository.save(scrapped_products)
            logger.info(f"Scraping completed. {updated_count} products updated.")
            self.notification.notify(f"Scraping completed. {updated_count} products updated.")
            return {"updated_count": updated_count}
        except Exception as e:
            logger.error(f"Failed to scrape: {str(e)}")
            self.notification.notify(f"Failed to scrape: {str(e)}")
            raise
