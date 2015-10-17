from crawler import crawler
from parser import parser
from mongo import saver
from redis.redis_db import RedisDataBase

from config import *


def main():
    site_crawler = crawler.Crawler(DOMAIN)
    collection = site_crawler.crawl()
    print len(collection.page_collection)
    data_saver = saver.DatabaseWorker()

    for url, content in collection.pages_content():
        nodes = parser.get_elements(content, REGULARS)
        nodes['url'] = url
        data_saver.save_item(nodes)
        RedisDataBase.save_to_db(result['url'], key)


if __name__ == "__main__":
    main()