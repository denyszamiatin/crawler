# -*- coding: utf-8 -*-
import unittest

from crawler.crawler import Crawler


class TestFindUrls(unittest.TestCase):

    def setUp(self):
        self.page = u"""
        <html>
        <head>
            <title>Смартфон Apple iPhone 6 16GB (Space Gray) | Hotline.ua</title>
            <link rel="stylesheet" type="text/css" media="all" href="/js/jquery/css/jquery.jscrollpane.css?v=2" />
            <link rel="stylesheet" type="text/css" href="/js/jquery/css/jquery-ui-1.8.12.custom.css?v=1" media="all" />
        </head>
        <body>
            <a href="http://www.hotline.ua/help/hl_checkout/" target="_blank">Подробнее о сервисе</a>
            <a href="http://www.hotline.ua/help/hl_checkout/h1/" target="_blank">Подробнее о сервисе</a>
            <a href="http://www.hotline.ua/help/hl_checkout/h3/#coverage" target="_blank">Подробнее о сервисе</a>
            <a href="/help/hl_checkout/h2/" target="_blank">Подробнее о сервисе</a>
            <a href="http://www.hotline.ua/help/hl_checkout/?list#coverage" target="_blank">Подробнее о сервисе</a>
            <a href="http://www.hotline.ua/help/hl_checkout/index.mp4" target="_blank">Подробнее о сервисе</a>
            <a href="http://www.hotline.ua/help/hl_checkout/index.jpg" target="_blank">Подробнее о сервисе</a>
        </body>
        </html>
        """

    def test_find_all_urls(self):
        c = Crawler('http://www.hotline.ua')
        expected_urls = [
            'http://www.hotline.ua/help/hl_checkout/h1/',
            'http://www.hotline.ua/help/hl_checkout/',
            'http://www.hotline.ua/help/hl_checkout/h3/',
            'http://www.hotline.ua/help/hl_checkout/h2/'
            ]
        self.assertEqual(sorted(c.find_all_urls(self.page)), sorted(expected_urls))

if __name__ == "__main__":
    unittest.main()
