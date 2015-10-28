# -*- coding: utf-8 -*-
from constants import IMAGE_LIST, IGNORE_LIST


class URLValidator(object):

    def __init__(self, url_list, domain):
        self.url_list = url_list
        self.domain = domain

    @staticmethod
    def is_not_correct_url(url):
        return "?" in url or len(url)<3 or \
               url.startswith("#") or \
               url.startswith("//")

    @staticmethod
    def is_in_list(url, lst):
        for item in lst:
            if item in url:
                return True
        else:
            return False

    def validate(self):

        if not self.domain.endswith("/"):
            self.domain += "/"

        checked_urls = []

        for url in self.url_list:

            if self.is_not_correct_url(url) or \
                    self.is_in_list(url, IGNORE_LIST)\
                    or self.is_in_list(url, IMAGE_LIST) or \
                    (url.startswith("http") and self.domain not in url):
                continue

            if "#" in url:
                url = url[:url.find("#")]

            if url.startswith("/"):
                checked_urls.append(self.domain + url[1:])

            elif url.startswith("http") and self.domain in url:
                checked_urls.append(url)

            else:
                checked_urls.append(self.domain + url)

        return checked_urls
