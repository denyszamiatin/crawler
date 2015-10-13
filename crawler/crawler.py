# -*- coding: utf-8 -*-
from lxml import html

import constants
import request
from log.log import log_error

DOMAIN = 'http://club-vulkan-777.com/'


class Crawler(object):

    def __init__(self, start_url):
        # Init vars
        self.domain = start_url
        self.queue = []
        self.parent_dict = {}
        self.available = 1

        response = request.get_request(start_url)

        if response is None:
            quit(log_error("Cannot start script."))

        # First item
        self.url_dict = self.get_page_description(response, start_url, start_url)

    @staticmethod
    def get_page_description(response, key_url, parent_url):
        return {
            key_url: {
                "is_checked": False,
                "code": response.status_code,
                "parent": parent_url,
                "content": response.text
            }
        }

    def increment_available(self):
        self.available += 1

    def add_urls(self, responses, url_dict):
        # Check for exist urls
        for response in responses:
            if response is None: continue

            if response.url not in url_dict:
                print(response.status_code, response.url, self.parent_dict.get(response.url))

                url_dict.update(
                    self.get_page_description(
                        response,
                        response.url,
                        self.parent_dict[response.url]
                    ))
                self.increment_available()

        return url_dict

    @staticmethod
    def filter_exist_urls(new_urls, url_dict):
        """
        Check for new urls
        """
        return [url for url in new_urls if url not in url_dict]

    def add_to_queue(self, new_urls, parent, url_dict):
        new_urls = self.filter_exist_urls(new_urls, url_dict)
        self.queue.extend(new_urls)
        self.parent_dict.update({url: parent for url in new_urls})

    @staticmethod
    def get_unique_list(old):
        return list(set(old))

    def get_list_queue(self):
        new_urls, self.queue = self.queue[:constants.THREADS], self.queue[constants.THREADS:]
        return new_urls

    def find_all_urls(self, page_source):
        # Initialize lxml parser
        page = html.fromstring(page_source)

        # Find start of link
        url_list = []
        url_list.extend(page.xpath('//a/@href'))
        url_list.extend(page.xpath('//link/@href'))

        url_list = self.get_unique_list(url_list)
        url_list = self.format_url_list(url_list)

        return url_list

    @staticmethod
    def is_not_correct_url(url):
        return "." in url or \
            "?" in url or \
            len(url) < 3 or \
            url.startswith("#") or \
            url.startswith("//")

    def format_url_list(self, url_list):
        if not self.domain.endswith("/"):
            self.domain += "/"

        # Delete doubles from list
        new_url_list = []

        # Find all valid relative links
        for url in url_list:

            url = url.strip()

            if self.is_not_correct_url(url):
                continue

            if "#" in url:
                url = url[:url.find("#")]

            if url.startswith("/"):
                new_url_list.append(self.domain + url[1:])

            elif url.startswith("http") and self.domain in url:
                new_url_list.append(url)

            elif url.startswith("http") and self.domain not in url:
                continue

            else:
                new_url_list.append(self.domain + url)

        return new_url_list

    def main_method(self, url_dict):
        dict_len = len(url_dict)

        # Start loop
        for url, params in url_dict.items():

            if dict_len == 1:
                print(params.get("code"), url)

            # Debug :)
            elif dict_len > 150:
                break

            if not params.get("is_checked"):

                # Get urls from page
                found_list = self.find_all_urls(params.get("content"))

                # Add new urls to queue
                self.add_to_queue(found_list, url, url_dict)

                if self.available > 0:
                    self.available -= 1

                if len(self.queue) >= constants.THREADS or self.available == 0:

                    # Get list for multi-thread check
                    new_list = self.get_list_queue()

                    # Get multi requests
                    result_array = request.get_multi_request(new_list)

                    # Add to url_dict
                    url_dict = self.add_urls(result_array, url_dict)

                # Update url in dict
                url_dict.get(url).update({"is_checked": True})
                url_dict = self.main_method(url_dict)

                return url_dict

        # Get redirect for urls
        return url_dict


if __name__ == "__main__":
    # Start script from main page
    crawler = Crawler(DOMAIN)
    outer_url_dict = crawler.main_method(crawler.url_dict)
    print len(outer_url_dict)
