# coding: utf-8
from lxml import html


def get_html_elements(page, regulars):
    """
    Функция парсинга html страницы по выражениям XPath
    :param page: Страница которую нужно парсить
    :param regulars: Словарь регулярных выражений XPath из файла 'regulars.py'
    :return: Словарь вида {название параметра: спаршенное значение}

    >>> HTML = '''<div title="buyer-name">Carson Busses</div>'''
    >>> regulars = {'byers': '//div[@title="buyer-name"]/text()'}
    >>> print get_html_elements(HTML, regulars)
    {'byers': ['Carson Busses']}
    """

    tree = html.fromstring(str(page))
    elements = {}
    for param in regulars.keys():
        elements[param] = tree.xpath(regulars[param])
    return elements
