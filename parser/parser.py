# coding: utf-8
from lxml import html


def get_elements(page, regulars):
    """
    Функция парсинга html страницы по выражениям XPath
    :param page: Страница которую нужно парсить
    :param regulars: Словарь регулярных выражений XPath из файла 'regulars.py'
    :return: Словарь вида {название параметра: спаршенное значение}

    >>> HTML = '''<div title="buyer-name">Carson Busses</div>'''
    >>> regulars = {'byers': '//div[@title="buyer-name"]/text()'}
    >>> print get_elements(HTML, regulars)
    {'byers': ['Carson Busses']}
    """
    tree = html.fromstring(page)
    return {page_element: tree.xpath(regulars[page_element]) for page_element in regulars}
