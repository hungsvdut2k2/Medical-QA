import json
from typing import List, Optional

import httpx


class DeepLTranslator:
    """
    A class that provides translation functionality using the DeepL API.

    Attributes:
        api_url (str): The URL of the DeepL translation API.
        headers (dict): The headers to be included in the API request.
    """
    def __init__(self):
        self.api_url = "http://127.0.0.1:1188/v2/translate"

        self.headers = {
            "Content-Type": "application/json",
        }

    def __call__(self, texts: List[str], src_language: Optional[str], dest_language: Optional[str]) -> List[str]:
        """
        Translate a list of texts using the DeepL API.

        Args:
            texts (List[str]): The list of texts to be translated.
            src_language (Optional[str]): The source language of the texts. If not provided, the API will detect the language automatically.
            dest_language (Optional[str]): The target language for the translation. If not provided, the API will use the default target language.

        Returns:
            List[str]: The translated messages as a list of strings.

        Raises:
            None
        """
        data = {
            "text": texts,
            "source_lang": src_language,
            "target_lang": dest_language,
        }

        post_data = json.dumps(data)
        response = httpx.post(url=self.api_url, data=post_data, headers=self.headers).json()
        translated_messages = response["translations"][0]["text"].split("\n")
        return translated_messages
