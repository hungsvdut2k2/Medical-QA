from typing import Any, List, Optional

import requests
from bs4 import BeautifulSoup
from loguru import logger

from .base_crawler import BaseCrawler


class DiseaseCrawler(BaseCrawler):
    def __init__(self, main_url: Optional[str]):
        super().__init__(main_url=main_url)

    def _crawl_urls(self) -> List[str]:
        urls = set()

        response = requests.get(self.main_url)
        soup = BeautifulSoup(response.text, "lxml")

        ul_tags = soup.find_all("ul", {"class": "collapsible-target"})

        for ul_tag in ul_tags:
            li_tags = ul_tag.find_all("li")
            for li_tag in li_tags:
                urls.add(li_tag.a["href"].split("/")[-2])
        return list(urls)

    def _crawl_content(self, url: Optional[str]) -> List[Any]:
        result = []
        url = self.main_url + url
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            sections = soup.find_all(
                "section", {"class": "collapsible-container collapsible-block collapsed screen-sm"}
            )

            for index, section in enumerate(sections):
                section_title = section.find("span").text
                section_content = section.find("div", {"class": "body collapsible-target"})

                p_tags = section_content.find_all("p")
                splitted_content = section_content.text.strip().split("\n")
                splitted_content = [content for content in splitted_content if content.strip() != ""]

                if len(p_tags) > 0:
                    if p_tags[0].strong:
                        splitted_content.pop(0)

                removed_start_index = 0

                if index == len(sections) - 1:
                    for content_index, line in enumerate(splitted_content):
                        if "Xem thêm:" in line:
                            removed_start_index = content_index

                if removed_start_index:
                    splitted_content = splitted_content[:removed_start_index]

                result.append(
                    {
                        "title": section_title,
                        "content": "\n".join(splitted_content),
                    }
                )
        except Exception as e:
            logger.error("{exception} at {url}".format(exception=e, url=url))

        return result
