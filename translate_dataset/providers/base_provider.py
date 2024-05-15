from abc import ABC, abstractmethod
from typing import Optional

from datasets import Dataset, load_dataset

from translate_dataset.translators import GoogleTranslator


class BaseProvider(ABC):
    def __init__(self, dataset_path: Optional[str], translator: GoogleTranslator, batch_size: Optional[int] = None):
        self.dataset_path = dataset_path
        self.translator = translator
        self.batch_size = batch_size
        self._load_dataset()

    def _load_dataset(self) -> Dataset:
        file_extension = str(self.dataset_path).split(".")[-1]
        if file_extension not in ["csv", "json", "jsonl"]:
            raise NotImplementedError("Unsupported file type")

        if file_extension == "jsonl":
            file_extension = "json"

        self.dataset = load_dataset(file_extension, data_files=self.dataset_path)["train"]

    def translate(self, src_language: Optional[str], dest_language: Optional[str]):
        return self._translate(src_language=src_language, dest_language=dest_language)

    @abstractmethod
    def _translate(self, src_language: Optional[str], dest_language: Optional[str]):
        pass
