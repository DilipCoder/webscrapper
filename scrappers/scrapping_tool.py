from abc import ABC, abstractmethod
from typing import Optional

class ScrappingTool(ABC):
    @abstractmethod
    async def get_html(self, url: str, proxy: Optional[str] = None) -> str:
        raise NotImplementedError