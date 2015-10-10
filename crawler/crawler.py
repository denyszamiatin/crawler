# -*- coding: utf-8 -*-
from lxml import html

import constants
import request
from log.log import log_error

DOMAIN = 'http://club-vulkan-777.com/'
domain = DOMAIN
queue = []
q_len = len(queue)
parent_dict = {domain: domain}
available = 1




def get_page_description(response, key_url, parent_url):
    return {
        key_url: {
            "is_checked": False,
            "code": response.status_code,
            "parent": parent_url,
            "content": response.text
        }
    }


def increment_available():
    global available
    available += 1


def init(start_url):
    #Init globals
    # global domain, queue, q_len, parent_dict, available

    response = request.get_request(start_url)

    if response is None:
        quit(log_error("Cannot start script."))

    #First item
    return get_page_description(response, start_url, start_url)


def add_urls(responses, url_dict):
    #Check for exist urls
    for response in responses:
        if response is None:
            continue

        if response.url not in url_dict:
            print(response.status_code, response.url, parent_dict.get(response.url))
            url_dict.update(get_page_description(
                response,
                response.url,
                parent_dict[response.url]
            ))
            increment_available()

    return url_dict


def filter_exist_urls(new_urls, url_dict):
    """
    Check for new urls
    """
    return [url for url in new_urls if url not in url_dict]


def add_to_queue(new_urls, parent, url_dict):
    new_urls = filter_exist_urls(new_urls, url_dict)
    queue.extend(new_urls)
    parent_dict.update({url: parent for url in new_urls})


def get_uniques(old):
    return list(set(old))


def get_list_queue():
    global queue
    new_urls, queue = queue[:constants.THREADS], queue[constants.THREADS:]
    return new_urls


def find_all_urls(page_source):
    #Initialize lxml parser
    page = html.fromstring(page_source)

    #Find start of link
    url_list = []
    url_list.extend(page.xpath('//a/@href'))
    url_list.extend(page.xpath('//link/@href'))

    url_list = format_url_list(get_uniques(url_list))

    return url_list


def is_not_correct_url(url):
    return "." in url or \
        "?" in url or \
        len(url) < 3 or \
        url.startswith("#") or \
        url.startswith("//")


def format_url_list(url_list):
    #Init globals
    global domain

    if not domain.endswith("/"):
        domain += "/"

   #Delete doubles from list
    new_url_list = []

    #Find all valid relative links
    for url in url_list:

        url = url.strip()

        if is_not_correct_url(url):
            continue

        if "#" in url:
            url = url[:url.find("#")]

        if url.startswith("/"):
            new_url_list.append(domain + url[1:])

        elif url.startswith("http") and domain in url:
            new_url_list.append(url)

        elif url.startswith("http") and domain not in url:
            continue

        else:
            new_url_list.append(domain + url)

    return new_url_list


def main_method(url_dict):
    #Init globals
    global queue, q_len, parent_dict, available
    dict_len = len(url_dict)

    #Start loop
    for url, params in url_dict.items():

        if dict_len == 1:
            print(params.get("code"), url)

        #Debug :)
        elif dict_len > 150:
            break

        if not params.get("is_checked"):

            #Get urls from page
            found_list = find_all_urls(params.get("content"))

            #Add new urls to queue
            add_to_queue(found_list, url, url_dict)

            if available > 0:
                available -= 1

            if len(queue) >= constants.THREADS or available == 0:

                #Get list for multi-thread check
                new_list = get_list_queue()

                #Get multi requests
                result_array = request.get_multi_request(new_list)

                #Add to url_dict
                url_dict = add_urls(result_array, url_dict)

            #Update url in dict
            url_dict.get(url).update({"is_checked": True})
            url_dict = main_method(url_dict)

            return url_dict

    #Get redirect for urls
    return url_dict


if __name__ == "__main__":
    #Start script from main page
    outer_url_dict = init(DOMAIN)
    outer_url_dict = main_method(outer_url_dict)
    print len(outer_url_dict)
