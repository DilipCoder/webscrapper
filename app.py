from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query
import uvicorn
from scrappers.web_scrapper import WebScrapper
from repositories.product_repository import ProductRepository
from notifications.console_notification import ConsoleNotification
from notifications.notification_manager import NotificationManager
from scrappers.product_scraper import ProductScrapper
from scrappers.playwright_scrapper import PlaywrightScraper
from repositories.notification_repository import NotificationRepository
from constants import AUTH_TOKEN
from fastapi.openapi.utils import get_openapi
from fastapi import Header

app = FastAPI()

notification_repository = NotificationRepository()

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
        scrapper=ProductScrapper(),
        scrapping_tool=PlaywrightScraper(),
        notification_manager=NotificationManager(),
    )
    return await scraper.scrape(proxy, pages, to_page, from_page)

@app.post("/add_user_to_topic")
async def add_user_to_topic(
    topic: str = Query("scraping", description="Topic to subscribe to", alias="topic_name"),
    user: str = Query("web_scrapper_user", description="User to add to the topic", alias="user"),
    authorization: str = Depends(authenticate)
):
    try:
        
        added_count = notification_repository.add(topic, user)
        if added_count > 0:
            return {"message": f"User '{user}' added to topic '{topic}' successfully."}
        else:
            raise HTTPException(status_code=400, detail="User already subscribed to this topic.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/add_users_to_topic")
async def add_users_to_topic(
    topic: str = Query(..., description="Topic to subscribe to"),
    users: list[str] = Query(..., description="Users to add to the topic"),
    authorization: str = Depends(authenticate)
):
    try:
        added_count = 0
        added_count = notification_repository.add_users_to_topic(topic, users)
        if added_count > 0:
            return {"message": f"Added {added_count} users to topic '{topic}' successfully."}
        else:
            raise HTTPException(status_code=400, detail="Users already subscribed to this topic.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/products")
async def get_products(authorization: str = Depends(authenticate)):
    repository = ProductRepository()
    return repository.get_all()

@app.get("/products/{product_id}")
async def get_product(product_id: str, authorization: str = Depends(authenticate)):
    repository = ProductRepository()
    return repository.get_product(product_id)

@app.get("/openapi.json", include_in_schema=False)
def get_openapi_json():
    return get_openapi(title="FastAPI Web Scraper", version="1.0.0", routes=app.routes)

if __name__ == '__main__':
    uvicorn.run(app, log_level="trace")