export PYTHONPATH=./

python translate_dataset/translate.py \
--provider-name instruction \
--input-file-path /Users/viethungnguyen/Medical-QA/dataset/medical_meadow_wikidoc.json \
--save-file-path /Users/viethungnguyen/Medical-QA/dataset/test.jsonl \
--src-language en \
--dest-language vi \
--batch-size 16