class PageCollection(object):
    def __init__(self, domain, response, parent_url):
        self.page_collection = {
            domain: {
                "is_checked": False,
                "code": response.status_code,
                "parent": parent_url,
                "content": response.text
            }
        }

    def add_page(self, response, url, parent_url):
        self.page_collection.update({
            url: {
                "is_checked": False,
                "code": response.status_code,
                "parent": parent_url,
                "content": response.text
            }})

    def add_pages(self, responses, parent_dict):
        for response in responses:

            # To avoid add exists url, we check and add returned url
            if not self.is_contain(response.url):
                self.add_page(response,
                              response.url,
                              parent_dict[response.url])

    def is_contain(self, url):
        return url in self.page_collection

    def get_available(self):
        return len([url for url, params in self.page_collection.items() if not params["is_checked"]])

    def set_checked(self, url):
        self.page_collection.get(url).update({"is_checked": True})

    def get_next_unchecked(self):
        for url in self.page_collection.keys():
            if not self.get_is_checked(url):
                yield url

    def get_is_checked(self, url):
        return self.page_collection.get(url).get("is_checked")

    def get_code(self, url):
        return self.page_collection.get(url).get("code")

    def get_parent(self, url):
        return self.page_collection.get(url).get("parent")

    def get_content(self, url):
        return self.page_collection.get(url).get("content")

    def get_len(self):
        return len(self.page_collection)

    def get_urls(self):
        return self.page_collection.keys()

    def __repr__(self):
        return u"\n".join([u"{} {}".format(self.get_code(url), url) for url in self.page_collection.keys()])
