export PYTHONPATH=./

python crawl_dataset/crawl.py \
--crawler-type disease \
--main-url https://www.vinmec.com/vi/benh/ \
--num-processes 2 \
--output-file-path /Users/viethungnguyen/Medical-QA/dataset/test.json