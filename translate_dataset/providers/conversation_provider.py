from typing import Optional

from tqdm import tqdm

from translate_dataset.translators import GoogleTranslator

from .base_provider import BaseProvider


class ConversationProvider(BaseProvider):
    """
    A class that provides translation functionality for conversations using the Google Translate API and DeepL API.

    Attributes:
        dataset_path (Optional[str]): The path to the dataset file.
        translator (GoogleTranslator): An instance of the GoogleTranslator class.
        batch_size (Optional[int]): The batch size for translation.
    """

    def __init__(self, dataset_path: Optional[str], translator: GoogleTranslator, batch_size: Optional[int]):
        super().__init__(dataset_path=dataset_path, batch_size=batch_size, translator=translator)
        self._load_dataset()

    def _translate(self, src_language: Optional[str], dest_language: Optional[str]):
        """
        Translate conversations from the source language to the destination language.

        Parameters:
            src_language (Optional[str]): The source language of the conversations. If not provided, the default language will be used.
            dest_language (Optional[str]): The destination language for translation. If not provided, the conversations will be translated to English.

        Returns:
            str: A string representation of the translated conversations.

        Note:
            This method uses the deepl_translator internally to translate the messages from the source language to English using the DeepL API. If the destination language is not English, it uses the GoogleTranslator class to further translate the messages to the desired language.

        Raises:
            None
        """
        self.dataset = self.dataset["input"]
        translated_result = []

        for index in tqdm(range(0, len(self.dataset), self.batch_size)):
            messages = self.dataset[index : index + self.batch_size]

            try:
                translated_message = self.translator(
                    texts=messages, src_language=src_language, dest_language=dest_language
                )

                translated_result.append({"conversation": translated_message})

            except Exception as e:
                print("Error")

        return translated_result
