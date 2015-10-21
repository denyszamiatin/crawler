from crawler import crawler
from parser import parser
from mongo import saver
from redis_db.redis_db import save_to_db

from config import *


def main():
    site_crawler = crawler.Crawler(DOMAIN)
    collection = site_crawler.crawl()
    print collection.get_len()
    data_saver = saver.DatabaseWorker()
    for url, content in collection.pages_content():
        nodes = parser.get_elements(content, REGULARS)
        data_saver.save_item(url, nodes)
        save_to_db(url, nodes)


if __name__ == "__main__":
    main()
