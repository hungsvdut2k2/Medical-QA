from typing import Optional
from tqdm import tqdm

from translate_dataset.translators import GoogleTranslator

from .base_provider import BaseProvider


class QuestionAnswerProvider(BaseProvider):
    """
    A class that provides translation functionality for question and answer datasets.

    Attributes:
        dataset_path (Optional[str]): The path to the dataset file.
        translator (GoogleTranslator): An instance of the GoogleTranslator class for translation functionality.
        batch_size (Optional[int]): The batch size for processing the dataset.
        dataset (Dataset): The loaded dataset.
    """
    def __init__(self, dataset_path: Optional[str], translator: GoogleTranslator, batch_size: Optional[int]):
        super().__init__(dataset_path=dataset_path, translator=translator, batch_size=batch_size)

    def _translate(self, src_language: Optional[str], dest_language: Optional[str]):
        """
        Translate the dataset from the source language to the destination language.

        Args:
            src_language (Optional[str]): The source language of the dataset. Defaults to None.
            dest_language (Optional[str]): The destination language for translation. Defaults to None.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing the translated questions and answers.

        Raises:
            None
        """
        translated_result = []

        for index in tqdm(range(0, len(self.dataset), self.batch_size)):
            batch_questions = self.dataset["question"][index: index + self.batch_size]
            batch_answers = self.dataset["answer"][index: index + self.batch_size]

            translated_questions = self.translator(texts=batch_questions, src_language=src_language, dest_language=dest_language)
            translated_answers = self.translator(texts=batch_answers, src_language=src_language, dest_language=dest_language)

            for question, answer in zip(translated_questions, translated_answers):
                translated_result.append({"question": question, "answer": answer})

        return translated_result
