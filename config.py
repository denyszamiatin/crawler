# coding: utf-8

import sys
sys.path.append('/home/sergei4e/itea/homework')

DATABASE = 'mongodb://localhost:27017/'

DOMAIN = 'http://allo.ua/'

REGULARS = {
    'покупатель': '//div[@title="buyer-name"]/text()',
    'цены': '//span[@class="item-price"]/text()',
    'компания': '//span[@class="item-company"]/text()',
    }
