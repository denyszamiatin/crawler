# -*- coding: utf-8 -*-
from lxml import html

import config
import request
import pages
from log.log import log_error
from url_validator import URLValidator


class Crawler(object):

    def __init__(self, start_url):
        # Init vars
        self.domain = start_url
        self.queue = []
        self.parent_dict = {}

    def start_crawling(self):
        response = request.get_request(self.domain)
        if response is None:
            quit(log_error("Cannot start script."))
        return pages.PageCollection(
            self.domain,
            response,
            self.domain
        )

    @staticmethod
    def filter_exist_urls(new_urls, page_collection):
        """
        Check for new urls
        """
        return [url for url in new_urls if url not in page_collection.get_urls()]

    def add_to_queue(self, new_urls, parent, page_collection):
        new_urls = self.filter_exist_urls(new_urls, page_collection)
        self.queue.extend(new_urls)
        self.parent_dict.update({url: parent for url in new_urls})

    def get_list_queue(self):
        new_urls, self.queue = self.queue[:config.THREADS], self.queue[config.THREADS:]
        return new_urls

    def find_all_urls(self, page_source):
        # Initialize lxml parser
        page = html.fromstring(page_source.encode('utf-8'))
        url_list = []

        # Find start of link
        url_list.extend(page.xpath('//a/@href'))
        url_list.extend(page.xpath('//link/@href'))

        # remove duplicates of urls
        url_list = set(url_list)

        # validate urls
        validation_input = URLValidator(url_list, self.domain)
        url_list = validation_input.validate()

        return url_list

    def crawl(self, page_collection=None):
        """
        Crawling page on site starting from domain
        :param page_collection: PageCollection instance
        :return: PageCollection instance
        """
        # First item
        if not page_collection:
            page_collection = self.start_crawling()

        # Start loop
        url = page_collection.get_next_unchecked()
        while url:

            if page_collection.get_len() == 1:
                print page_collection.pages[url].get_code(), url

            # Debug :)
            elif page_collection.get_len() > config.MAX_URLS:
                break

            # Get urls from page
            urls_to_check = self.find_all_urls(page_collection.pages[url].get_content())

            # Add new urls to queue
            self.add_to_queue(urls_to_check, url, page_collection)

            if len(self.queue) >= config.THREADS or not page_collection.is_available():

                # Get list for multi-thread check
                new_list = self.get_list_queue()

                # Get multi requests
                responses = request.get_multi_request(new_list)

                # Add to url_dict
                page_collection.add_pages(responses, self.parent_dict)

            # Update url in dict
            page_collection.pages[url].set_checked()
            url = page_collection.get_next_unchecked()
            print "Fetching {}".format(url)

        # Get redirect for urls
        return page_collection

if __name__ == "__main__":
    # Start script from main page
    crawler = Crawler(config.DOMAIN)
    collection = crawler.crawl()
    print collection.get_len()
    print collection
