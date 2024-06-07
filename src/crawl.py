import argparse
import json
from multiprocessing import Pool

from tqdm import tqdm

from crawl_dataset.crawlers.crawler_factory import CrawlerFactory

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawler-type", type=str, required=True)
    parser.add_argument("--main-url", type=str, required=True)
    parser.add_argument("--num-processes", type=int, required=True)
    parser.add_argument("--output-file-path", type=str, required=True)
    args = parser.parse_args()

    crawler = CrawlerFactory.create_crawler(
        crawler_type=args.crawler_type, main_url=args.main_url
    )

    urls = crawler.crawl_urls()

    with Pool(args.num_processes) as pool:
        results_iter = list(
            tqdm(pool.imap(crawler.crawl_content, urls), total=len(urls))
        )

    final_contents = []

    for content in results_iter:
        if len(content) > 0:
            final_contents.extend(content)


    with open(args.output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(final_contents, json_file, ensure_ascii=False, indent=4)


