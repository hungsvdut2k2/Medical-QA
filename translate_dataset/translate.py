import argparse
import json
from translate_dataset.providers import ProviderFactory
from translate_dataset.translators import GoogleTranslator

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file-path", type=str, required=True, help="Your input dataset file path, can be in huggingface")
    parser.add_argument("--provider-name", type=str, required=True, help="Type of your using dataset")
    parser.add_argument("--src-language", type=str, required=True, help="The source language of your using dataset")
    parser.add_argument("--dest-language", type=str, required=True, help="The destination language of your using dataset")
    parser.add_argument("--save-file-path", type=str, required=True, help="The path to save the translated dataset")
    parser.add_argument("--batch-size", type=int, required=True, help="Batch Size for batch processing")

    arguments = parser.parse_args()

    google_translator = GoogleTranslator()
    factory = ProviderFactory()
    provider = factory.get_provider(provider_name=arguments.provider_name, dataset_path=arguments.input_file_path, translator=google_translator, batch_size=arguments.batch_size)
    results = provider.translate(src_language=arguments.src_language, dest_language=arguments.dest_language)

    with open(arguments.save_file_path, 'w', encoding="utf-8") as file:
        for item in results:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')
