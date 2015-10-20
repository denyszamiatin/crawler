class Page(object):

    def __init__(self, response, parent_url):
        self.url = response.url
        self.url_is_checked = False
        self.code = response.status_code
        self.parent = parent_url
        self.content = response.text

    def get_url(self):
        return self.url

    def is_checked(self):
        return self.url_is_checked

    def get_code(self):
        return self.code

    def get_parent(self):
        return self.parent

    def get_content(self):
        return self.content

    def set_checked(self):
        self.url_is_checked = True
