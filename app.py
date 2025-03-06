from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query
import uvicorn;
from scrappers.web_scrapper import WebScrapper
from repositories.product_repository import ProductRepository
from notifications.console_notification import ConsoleNotification
from scrappers.product_scraper import ProductScrapper
from scrappers.playwright_scrapper import PlaywrightScraper
from constants import AUTH_TOKEN
from fastapi.openapi.utils import get_openapi
from fastapi import Header

app = FastAPI()


def authenticate(authorization: str = Header("Bearer d2ViYWNjZXNzCg", description="Bearer token for authentication")):
    token = authorization.replace("Bearer ", "")
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/scrape")
async def scrape(
    from_page: int = Query(1, gt=0, description="Page to start scraping"),
    to_page: Optional[int] = Query(1, gt=0, description="Page to end scraping"),
    pages: Optional[int] = Query(1, gt=0, description="Number of pages to scrape"),
    proxy: Optional[str] = Query(None, description="Proxy URL"),
    authorization: str = Depends(authenticate)
):
    scraper = WebScrapper(
        base_url="https://dentalstall.com/shop/page/{}/",
        repository=ProductRepository(storage=None),
        notification=ConsoleNotification(),
        scrapper=ProductScrapper(),
        scrapping_tool=PlaywrightScraper()
    )
    return await scraper.scrape(proxy, pages, to_page, from_page)

@app.get("/openapi.json", include_in_schema=False)
def get_openapi_json():
    return get_openapi(title="FastAPI Web Scraper", version="1.0.0", routes=app.routes)

if __name__ == '__main__':
    uvicorn.run(app, log_level="trace")