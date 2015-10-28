# coding: utf-8

import sys
sys.path.append('/home/sergei4e/itea/homework')

DATABASE = 'mongodb://localhost:27017/'

DOMAIN = 'http://allo.ua/'

REGULARS = {
    'title': '//title/text()'
    # 'покупатель': '//div[@title="buyer-name"]/text()',
    # 'цены': '//span[@class="item-price"]/text()',
    # 'компания': '//span[@class="item-company"]/text()',
    }

MAX_URLS = 100

THREADS = 20

# Images
IMAGE_LIST = [
    ".ico", ".ICO", ".gif", ".GIF", ".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".bmp", ".BMP"
]

IGNORE_LIST = [
    ".mp4", ".webm", ".apk", ".ogv", ".swf", ".svg", ".eot", ".ttf", ".woff", "javascript:", "data:", "mailto:",
    "mail.ru", "livejournal", "@", ">", "<", ".zip", "7z", ".rar", ".exe", ".pl", ".pdf", ".css", ".js"
]