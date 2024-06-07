from typing import Optional

from .base_crawler import BaseCrawler
from .disease_crawler import DiseaseCrawler
from .medicine_crawler import MedicineCrawler


class CrawlerFactory:
    @staticmethod
    def create_crawler(crawler_type: Optional[str], **kwargs) -> BaseCrawler:
        crawler_dict = {"disease": DiseaseCrawler, "medicine": MedicineCrawler}
        if crawler_type in crawler_dict.keys():
            return crawler_dict[crawler_type](**kwargs)
        raise ValueError("Invalid crawler type")
