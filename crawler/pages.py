from log import log
import page


class PageCollection(object):
    def __init__(self, domain, response, parent_url):
        self.pages = {}
        self.add_page(response, domain, parent_url)

    def add_page(self, response, url, parent_url):
        self.pages[url] = page.Page(response, parent_url)

    def add_pages(self, responses, parent_dict):
        for response in responses:
            # To avoid add exists url, we check and add returned url
            try:
                if not self.is_contain(response.url):
                    self.add_page(response,
                                  response.url,
                                  parent_dict[response.url])
            except KeyError:
                log.log_error("{} doesn't exist".format(response.url))

    def is_contain(self, url):
        return url in self.pages

    def is_available(self):
        return [url for url in self.pages if not self.pages[url].is_checked()]

    def get_next_unchecked(self):
        for url in self.pages:
            if not self.pages[url].is_checked():
                return url
        return ''

    def is_valid_page(self, url):
        return self.pages[url].get_code() == 200

    def get_len(self):
        return len(self.pages)

    def get_urls(self):
        return self.pages.keys()

    def pages_content(self):
        for url in self.pages:
            if self.is_valid_page(url):
                yield url, self.pages[url].get_content()

    def __repr__(self):
        return u"\n".join([u"{} {}".format(self.pages[url].get_code(), url) for url in self.pages.keys()])
