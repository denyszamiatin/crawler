# -*- coding: utf-8 -*-
import multiprocessing

import requests

import config
from log.log import logger
__author__ = 'dzamakhaiev'

requests.packages.urllib3.disable_warnings()


def get_request(url):
    """
    Gets request by url
    """
    try:
        return requests.get(url, verify=False)
    except (
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
        requests.exceptions.RequestException
    ) as e:
        logger.error("{}\n {}".format(e, url))


def get_multi_request(urls):
    """
    Gets many requests in THREADS processes
    :param urls:
    :return:
    """
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=config.THREADS)
    pages = pool.map(get_request, urls)
    pool.close()

    return pages
