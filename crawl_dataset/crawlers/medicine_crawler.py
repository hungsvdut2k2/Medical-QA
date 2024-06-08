from typing import Any, List, Optional

from .base_crawler import BaseCrawler


class MedicineCrawler(BaseCrawler):
    def __init__(self, main_url: Optional[str]):
        super().__init__(main_url=main_url)

    def _crawl_urls(self) -> List[str]:
        return []

    def _crawl_content(self, url: List[str]) -> List[Any]:
        return []
