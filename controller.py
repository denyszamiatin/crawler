from crawler import crawler
from parser import parser
from mongo import saver
from redis.redis_db import RedisDataBase

from config import *


def main():
    site_crawler = crawler.Crawler(DOMAIN)
    collection = site_crawler.main_method()
    data_saver = saver.DatabaseWorker()

    for key, value in collection.items():
        result = parser.get_elements(value['content'], REGULARS)
        result['url'] = key
        data_saver.save_item(result)
        RedisDataBase.save_to_db(result['url'], key)

if __name__ == "__main__":
    main()