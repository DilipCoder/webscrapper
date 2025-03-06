from typing import Optional
from playwright.async_api import async_playwright
from .scrapping_tool import ScrappingTool

class PlaywrightScraper(ScrappingTool):
    def __init__(self):
        self.browser = None

    async def start_browser(self, proxy: Optional[str] = None):
        if not self.browser:
            playwright = await async_playwright().start()
            launch_options = {"headless": True}
            if proxy:
                launch_options["proxy"] = {"server": proxy}
            self.browser = await playwright.chromium.launch(**launch_options)

    async def get_html(self, url: str, proxy: Optional[str] = None) -> str:
        await self.start_browser(proxy=proxy)
        page = await self.browser.new_page()
        await page.goto(url)
        html = await page.content()
        await page.close()
        return html

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
