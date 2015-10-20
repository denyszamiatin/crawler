# -*- coding: utf8 -*-
import unittest
import redis

from redis_db.redis_db import save_to_db


class DataBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.test_db_client = redis.Redis(host='localhost', port=6379, db=0)
        self.key = u"http://allo.ua/stroitel-nye-tachki/"
        self.value = u"{'url': u'http://allo.ua/stroitel-nye-tachki/', '_id': ObjectId('5626b5df6ae6c76340a0a32e')}"

    def test_save_to_db(self):
        save_to_db(self.key, self.value)
        self.assertEqual(self.test_db_client.get(self.key), self.value)

    def tearDown(self):
        self.test_db_client.flushdb()

