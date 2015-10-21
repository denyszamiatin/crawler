# coding: utf-8
from pymongo import MongoClient

from config import *


class DatabaseWorker(object):
    """
    Класс DatabaseWorker создает соединение с базой данных Mongodb.
    Метод save(data) сохраняет в базу словарь data

    >>> data = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python"]}
    >>> s = DatabaseWorker()
    >>> s.save_item(data)
    ObjectId(...)
    """

    client = MongoClient(DATABASE)
    db = client.goods

    @staticmethod
    def save_item(url, nodes):
        nodes['url'] = url
        return DatabaseWorker.db.items.insert_one(nodes).inserted_id
