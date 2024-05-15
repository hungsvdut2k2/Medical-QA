from abc import ABC, abstractmethod
from typing import Optional

from datasets import Dataset, load_dataset

from translate_dataset.translators import GoogleTranslator


class BaseProvider(ABC):
    """
    A base abstract class for providers that handle translation tasks.

    Attributes:
        dataset_path (Optional[str]): The path to the dataset file.
        translator (GoogleTranslator): An instance of the GoogleTranslator class for translation functionality.
        batch_size (Optional[int]): The batch size for processing the dataset.
        dataset (Dataset): The loaded dataset.
    """
    def __init__(self, dataset_path: Optional[str], translator: GoogleTranslator, batch_size: Optional[int] = None):
        self.dataset_path = dataset_path
        self.translator = translator
        self.batch_size = batch_size
        self._load_dataset()

    def _load_dataset(self) -> Dataset:
        """
        Load the dataset from the specified file.

        Returns:
            Dataset: The loaded dataset.

        Raises:
            NotImplementedError: If the file type is not supported.
        """
        file_extension = str(self.dataset_path).split(".")[-1]
        if file_extension not in ["csv", "json", "jsonl"]:
            raise NotImplementedError("Unsupported file type")

        if file_extension == "jsonl":
            file_extension = "json"

        self.dataset = load_dataset(file_extension, data_files=self.dataset_path)["train"]

    def translate(self, src_language: Optional[str], dest_language: Optional[str]):
        """
        Translate the dataset from the source language to the destination language.

        Args:
            src_language (Optional[str]): The source language of the dataset. Defaults to None.
            dest_language (Optional[str]): The destination language for translation. Defaults to None.

        Returns:
            None

        Raises:
            NotImplementedError: If the translation functionality is not implemented in the child class.
        """
        return self._translate(src_language=src_language, dest_language=dest_language)

    @abstractmethod
    def _translate(self, src_language: Optional[str], dest_language: Optional[str]):
        pass
