from typing import Optional

from tqdm import tqdm

from src.translate_dataset.translators import GoogleTranslator

from .base_provider import BaseProvider


class InstructionProvider(BaseProvider):
    def __init__(self, dataset_path: Optional[str], translator: GoogleTranslator, batch_size: Optional[str]):
        super().__init__(dataset_path=dataset_path, translator=translator, batch_size=batch_size)

    def _translate(self, src_language: Optional[str], dest_language: Optional[str]) -> str:
        translated_result = []
        translated_instruction = self.translator(
            texts=[self.dataset["instruction"][0]], src_language=src_language, dest_language=dest_language
        )

        for index in tqdm(range(0, len(self.dataset), self.batch_size)):
            batch_questions = self.dataset["input"][index : index + self.batch_size]
            batch_answers = self.dataset["output"][index : index + self.batch_size]

            translated_questions = self.translator(
                texts=batch_questions, src_language=src_language, dest_language=dest_language
            )
            translated_answers = self.translator(
                texts=batch_answers, src_language=src_language, dest_language=dest_language
            )

            for question, answer in zip(translated_questions, translated_answers):
                translated_result.append(
                    {"instruction": translated_instruction[0], "question": question, "answer": answer}
                )

        return translated_result
