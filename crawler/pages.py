from log import log


class PageCollection(object):
    def __init__(self, domain, response, parent_url):
        self.page_collection = {}
        self.add_page(response, domain, parent_url)

    def add_page(self, response, url, parent_url):
        self.page_collection.update({
            url: {
                "is_checked": False,
                "code": response.status_code,
                "parent": parent_url,
                "content": response.text
            }
        })

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
        return url in self.page_collection

    def is_available(self):
        return [url for url in self.page_collection if not self.is_checked(url)]

    def set_checked(self, url):
        self.page_collection[url]["is_checked"] = True

    def get_next_unchecked(self):
        for url in self.page_collection:
            if not self.is_checked(url):
                return url
        return ''

    def is_checked(self, url):
        return self.page_collection[url]["is_checked"]

    def is_valid_page(self, url):
        return self.page_collection[url]["code"] == 200

    def get_parent(self, url):
        return self.page_collection.get(url).get("parent")

    def get_content(self, url):
        return self.page_collection[url]["content"]

    def get_len(self):
        return len(self.page_collection)

    def get_urls(self):
        return self.page_collection.keys()

    def pages_content(self):
        for url in self.page_collection:
            if self.is_valid_page(url):
                yield url, self.get_content(url)

    def __repr__(self):
        return u"\n".join([u"{} {}".format(self.get_code(url), url) for url in self.page_collection.keys()])
