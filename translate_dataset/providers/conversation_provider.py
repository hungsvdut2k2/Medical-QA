import json
from typing import List, Optional

import httpx
from tqdm import tqdm

from translate_dataset.translators import DeepLTranslator, GoogleTranslator


class ConversationProvider:
    """
    A class that provides translation functionality for conversations using the Google Translate API and DeepL API.

    Attributes:
        dataset_path (Optional[str]): The path to the dataset file.
        translator (GoogleTranslator): An instance of the GoogleTranslator class.
        batch_size (Optional[int]): The batch size for translation.
    """

    def __init__(self, dataset_path: Optional[str], translator: GoogleTranslator, batch_size: Optional[int]):
        self.dataset_path = dataset_path
        self.translator = translator
        self.deepl_translator = DeepLTranslator()
        self.batch_size = batch_size
        self._load_dataset()

    def _load_dataset(self):
        """
        Load the dataset from the specified dataset path.

        This method reads the dataset file from the given dataset path and stores it in the 'dataset' attribute of the ConversationProvider class.

        Parameters:
            None

        Returns:
            None
        """
        dataset = json.load(open(self.dataset_path))
        self.dataset = dataset

    def translate(self, src_language: Optional[str], dest_language: Optional[str]) -> str:
        """
        Translate conversations from the source language to the destination language.

        Parameters:
            src_language (Optional[str]): The source language of the conversations. If not provided, the default language will be used.
            dest_language (Optional[str]): The destination language for translation. If not provided, the conversations will be translated to English.

        Returns:
            str: A string representation of the translated conversations.

        Note:
            This method uses the _translate method internally to perform the actual translation.)
        """
        return self._translate(src_language=src_language, dest_language=dest_language)

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
        translated_result = []
        for index in tqdm(range(0, len(self.dataset))):
            conversation = {"role": [], "message": []}

            for message in self.dataset[index]:
                splitted_message = message.split("：")

                if splitted_message[0] == "医生":
                    conversation["role"].append("assistant")
                else:
                    conversation["role"].append("user")

                conversation["message"].append(splitted_message[1])

            translated_message = self.deepl_translator(
                texts=conversation["message"], src_language=src_language, dest_language="en"
            )

            if dest_language != "en":
                translated_message = self.translator(texts=[], src_language="en", dest_language=dest_language)

            translated_conversation = []

            for role, message in zip(conversation["role"], translated_message):
                translated_conversation.append({"role": role, "content": message})

            translated_result.append({"conversation": translated_conversation})

        return translated_result
