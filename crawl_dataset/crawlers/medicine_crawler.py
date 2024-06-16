from typing import Any, List, Optional
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

from selenium.webdriver.common.by import By
from loguru import logger

from .base_crawler import BaseCrawler
from crawl_dataset.driver.chrome_driver import chrome_driver


class MedicineCrawler(BaseCrawler):
    def __init__(self, main_url: Optional[str]):
        super().__init__(main_url=main_url)

    def _crawl_urls(self) -> List[str]:
        urls = []
        response = requests.get(self.main_url)
        soup = BeautifulSoup(response.text, "lxml")
        num_pages = soup.find("span", {"class": "current"}).text.split("/")[1]

        for i in tqdm(range(1, int(num_pages) + 1)):
            response = requests.get(self.main_url.split("=")[0] + "=" + str(i))
            soup = BeautifulSoup(response.text, "lxml")
            latest_post = soup.find("h2", {"class": "title-latest-post"})
            urls.append(latest_post.a["href"])

            post_content_tags = soup.find_all("div", {"class": "post-content"})

            for tag in post_content_tags:
                h2_tag = tag.find("h2")
                urls.append(h2_tag.a["href"])

        return urls

    def _crawl_content(self, url: Optional[str]) -> List[Any]:
        url = "/".join(self.main_url.split("/")[:-3]) + url
        result = []
        chrome_driver.get(url)
        try:
            read_more_button = chrome_driver.find_element(By.ID, "readmore_content")
            read_more_button.click()

        except:
            pass

        try:
            main_content_tag = chrome_driver.find_element(By.CLASS_NAME, "block-content.cms.pageview-highest")
            main_html = main_content_tag.get_attribute("innerHTML")
            split_content = self._remove_html_tags_with_newlines(html=main_html).split("\n")
            start_indices = self._get_start_indices(split_content=split_content)
            chunks = self._chunk_content(url=url, content=split_content, start_indices=start_indices)
            result.extend(chunks)

        except Exception as e:
            logger.debug(f"{e} at {url}")

        return result

    def _remove_html_tags_with_newlines(self, html):
        # Define a regex pattern to match HTML tags
        tag_re = re.compile(r"<[^>]+>")

        # Replace all tags with a newline character
        text_with_newlines = tag_re.sub("\n", html)

        # Optional: Clean up multiple newlines to a single newline
        # This step is to ensure that we don't have unnecessary blank lines
        text_cleaned = re.sub(r"\n+", "\n", text_with_newlines)

        # Strip leading/trailing newlines
        return text_cleaned.strip()

    def _starts_with_decimal_pattern(self, sentence: Optional[str]) -> bool:
        # Define a regex pattern to match numbers like 2., 2.1, 2.123, etc., at the start of the sentence
        pattern = re.compile(r"^\d+\.\d*")

        # Search for the pattern at the start of the sentence
        match = pattern.match(sentence)

        # Return True if a match is found, else False
        return match is not None

    def _get_start_indices(self, split_content: List[str]) -> List[int]:
        start_indices = []
        for index, content in enumerate(split_content):
            if self._starts_with_decimal_pattern(content):
                start_indices.append(index)

        return start_indices

    def _chunk_content(self, url: Optional[str], content: List[str], start_indices: List[int]) -> List[Any]:
        chunks = []
        removed_pattern = ["Trên đây là toàn bộ thông tin về", "XEM THÊM:", "Nguồn tham khảo"]

        for index, line in enumerate(start_indices[:-1]):
            chunks.append(
                {
                    "url": url,
                    "title": content[start_indices[index]],
                    "content": "\n".join(content[start_indices[index]:start_indices[index + 1]]),
                }
            )

        removed_indices = 0

        for index, line in enumerate(content):
            for pattern in removed_pattern:
                if pattern in line:
                    removed_indices = index
                    break

        chunks.append(
            {
                "url": url,
                "title": content[start_indices[-1]],
                "content": "\n".join(content[start_indices[-1]:removed_indices]),
            }
        )

        return chunks
