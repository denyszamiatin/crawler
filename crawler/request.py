# -*- coding: utf-8 -*-
import requests
import multiprocessing
import constants
__author__ = 'dzamakhaiev'

requests.packages.urllib3.disable_warnings()


def get_request(url):
        try:
            req = requests.get(url, verify=False)
            return req

        except Exception as e:
            print(e, url)
            return None


def multi_request(new_list):
    #Prepare multi
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=constants.THREADS)

    result_array = pool.map(get_request, new_list)
    pool.close()

    return result_array
