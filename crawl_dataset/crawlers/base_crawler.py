from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseCrawler(ABC):
    def __init__(self, main_url: Optional[str]):
        self.main_url = main_url

    def crawl_urls(self) -> List[str]:
        return self._crawl_urls()

    @abstractmethod
    def _crawl_urls(self) -> List[str]:
        pass

    def crawl_content(self, url: List[str]) -> List[Any]:
        return self._crawl_content(url=url)

    @abstractmethod
    def _crawl_content(self, url: List[str]) -> List[Any]:
        pass
