from crawler import crawler
import unittest
import mock

START_URL = "http://club-vulkan-777.com/"
TEST_PAGE = """
<!DOCTYPE html>
<html lang="ru-RU" prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb#">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>None</title>
<link rel="pingback" href="http://club-vulkan-777.com/xmlrpc.php" />
<link rel="wrong_url" href="http://google.com"/>
<link rel="stylesheet" href="http://club-vulkan-777.com/wp-content/themes/expound/style.css" type="text/css" media="screen"/>
<link rel="Shortcut Icon" href="http://club-vulkan-777.com/wp-content/themes/expound/favicon.ico" type="image/x-icon" />
<link rel='prev' title='test 1' href='http://club-vulkan-777.com/instant-bonuses/'/>
<link rel='next' title='test 2' href='http://club-vulkan-777.com/the-golden-age/'/>
</head>
<body>
</body>
"""


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = crawler.Crawler(START_URL)

    def test_find_all_urls(self):
        urls = self.crawler.find_all_urls(TEST_PAGE)
        expected_urls_number = 3
        self.assertEqual(expected_urls_number, len(urls),
                         "From test page found unexpected number of urls.\n"
                         "Expected value: {}. Actual value: {}".format(expected_urls_number, len(urls)))

    def test_add_double(self):
        page_collection = self.crawler.start_crawling()
        response = mock.Mock(url=START_URL, status_code=200, text="")
        page_collection.add_pages(responses=(response,), parent_dict={START_URL: START_URL})
        expected_pages = 1
        self.assertEqual(expected_pages, page_collection.get_len(),
                         "Unexpected pages in collection after add double page.\n"
                         "Expected value: {}. Actual value: {}".format(expected_pages, page_collection.get_len()))

    def test_add_new(self):
        page_collection = self.crawler.start_crawling()
        new_url = 'http://club-vulkan-777.com/the-golden-age/'
        response = mock.Mock(url=new_url, status_code=200, text="")
        page_collection.add_pages(responses=(response,), parent_dict={new_url: START_URL})
        expected_pages = 2
        self.assertEqual(expected_pages, page_collection.get_len(),
                         "Unexpected pages in collection after add new page.\n"
                         "Expected value: {}. Actual value: {}".format(expected_pages, page_collection.get_len()))


if __name__ == '__main__':
    unittest.main()
