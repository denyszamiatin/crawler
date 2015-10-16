from crawler import crawler
from parser import parser
from mongo import saver

from config import *


def main():
    site_crawler = crawler.Crawler(DOMAIN)
    outer_url_dict = site_crawler.main_method(site_crawler.url_dict)
    data_saver = saver.DatabaseWorker()

    for key, value in outer_url_dict.items():
        result = parser.get_elements(value['content'], REGULARS)
        result['url'] = key
        data_saver.save_item(result)


if __name__ == "__main__":
    main()