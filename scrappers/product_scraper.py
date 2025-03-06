from .scrapper_strategy import ScrapperStrategy
from typing import List
from models.product_model import Product
from bs4 import BeautifulSoup
from utils.logger import logger
from utils.currency_mapping import CURRENCY_MAPPING
import re

class Selectors:
    page_title = "head > title"
    product_container = "#mf-shop-content > ul > li"
    product_title = "div.mf-product-content > h2 > a"
    product_price = "div.mf-product-price-box > span.price > span.woocommerce-Price-amount > bdi, div.mf-product-price-box > span.price > ins > span > bdi"

class ProductScrapper(ScrapperStrategy):
    def __init__(self):
        self.selectors = Selectors

    def get_page_no(self, title: str) -> int | str:
        match = re.search(r'Page (\d+)', title)
        page_no = 1
        try:
            page_no = int(match.group(1))
        except Exception as e:
            page_no = title
        return page_no
    
    def extract_price_and_currency(self, price_text: str) -> tuple[float, str]:
        for symbol, code in CURRENCY_MAPPING.items():
            if symbol in price_text:
                price = float(price_text.replace(symbol, '').replace(',', '').strip())
                return price, code
        return float(price_text.replace(',', '').strip()), "UNKNOWN"

    async def parse_page(self, html) -> List[Product]:
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        title = soup.select_one(self.selectors.page_title).text
        page_no = self.get_page_no(title)
        logger.info(f"Scraping page: {title}")
        container = soup.select(self.selectors.product_container)
        for i in range(len(container)):
            try:
                logger.debug(f"Processing page: {page_no} product {i}")
                item = container[i]
                image = item.select("img")[0]["src"]
                title_obj = item.select_one(self.selectors.product_title)
                title = title_obj["href"].split("/")[-2]
                price_obj = item.select_one(self.selectors.product_price)
                price_text = price_obj.text if price_obj else "N/A"
                price, currency = self.extract_price_and_currency(price_text)
                product = Product(title=title, price=price, currency=currency, image_url=image)
                products.append(product)
            except Exception as e:
                logger.error(f"Error processing page: {page_no} product {i}: {e}")
        logger.info(f"Scraped {len(products)} products from {title}")
        return products
