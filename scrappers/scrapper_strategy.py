from abc import ABC, abstractmethod
from typing import List

class ScrapperStrategy(ABC):
    @abstractmethod
    async def parse_page(self, html: str, *args, **kwargs) -> List:
        pass