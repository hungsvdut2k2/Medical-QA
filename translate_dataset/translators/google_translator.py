from typing import List, Optional

from googletrans import Translator


class GoogleTranslator:
    """
    A class that provides translation functionality using the Google Translate API.

    Attributes:
        translator (googletrans.Translator): An instance of the Google Translate API translator.
    """

    def __init__(self):
        self.translator = Translator()

    def __call__(self, texts: List[str], src_language: Optional[str], dest_language: Optional[str]) -> List[str]:
        """
        Translate a list of texts from a source language to a destination language using the Google Translate API.

        Args:
            texts (List[str]): A list of texts to be translated.
            src_language (Optional[str]): The source language of the texts. If not provided, the API will attempt to detect the language.
            dest_language (Optional[str]): The destination language for the translation. If not provided, the API will use the default target language.

        Returns:
            List[str]: A list of translated texts.

        Raises:
            None
        """
        translated_objects = self.translator.translate(texts, src=src_language, dest=dest_language)
        translated_texts = [translated_object.text for translated_object in translated_objects]
        return translated_texts
