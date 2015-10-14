class Page(object):

    def __init__(self, response, parent_url):
        self.is_checked = False
        self.code = response.status_code
        self.parent = parent_url
        self.content = response.text

