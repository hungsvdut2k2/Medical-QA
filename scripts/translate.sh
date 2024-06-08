export PYTHONPATH=./

python src/translate.py \
	--provider-name conversation \
	--input-file-path /Users/viethungnguyen/Medical-QA/dataset/dialouge_dataset/medical_chat_data.json \
	--save-file-path /Users/viethungnguyen/Medical-QA/dataset/translated/medical_chat_data.jsonl \
	--src-language en \
	--dest-language vi \
	--batch-size 16