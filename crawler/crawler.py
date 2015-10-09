# -*- coding: utf-8 -*-
import constants
import request
from lxml import html
__author__ = 'dzamakhaiev'


#Glogal vars
domain = None
queue = None
q_len = None
parent_dict = None
available = None
DOMAIN = 'http://club-vulkan-777.com/'


def init(start_url):
    #Init globals
    global domain, queue, q_len, parent_dict, available

    #Set start url
    domain = start_url
    queue = []
    q_len = len(queue)
    parent_dict = {domain: domain}
    available = 1

    req = request.get_request(domain)

    if req is None:
        quit("Cannot start script.")

    #First item
    url_dict = \
        {
            domain:
                {
                    "is_checked": False,
                    "code": get_status_code(req),
                    "parent": domain,
                    "content": get_content(req)
                }
        }

    return url_dict


def add_to_dict(result_array, url_dict):
    #Init globals
    global parent_dict, available

    #Check for exist urls
    for url_req in result_array:

        req = url_req
        if req is None:
            continue
        else:
            parent = parent_dict.get(req.url)

        if req.url not in url_dict:
            print(req.status_code, req.url, parent)

            url_dict.update({
                req.url:
                    {
                        "is_checked": False,
                        "code": get_status_code(req),
                        "parent": parent,
                        "content": get_content(req),
                    }})
            available += 1

    return url_dict


def add_to_queue(found_list, parent, url_dict):
    #Init globals
    global queue, q_len, parent_dict

    #Check for new urls
    for found_url in found_list:
        if found_url in url_dict:
            pass
        else:
            queue.append(found_url)

    q_len = len(queue)

    #Add to parent dict
    for found_url in found_list:
        if found_url not in url_dict:
            parent_dict.update({found_url: parent})


def delete_doubles_from_list(old_list):
    buf_set = set(old_list)
    new_list = list(buf_set)
    return new_list


def delete_from_queue(new_list):
    #Init globals
    global queue, q_len

    #Delete chosen urls from queue
    for new_url in new_list:
        queue.remove(new_url)

    q_len = len(queue)


def get_list_queue():
    #Init globals
    global queue
    new_list = []

    #Get url list for check
    for new_url in queue:

        if len(new_list) >= constants.THREADS:
            break
        else:
            new_list.append(new_url)

    #Delete chosen urls from queue
    delete_from_queue(new_list)

    return new_list


def get_status_code(req):
    return req.status_code


def get_content(req):
    return req.text


def find_all_urls(page_source):
    url_list = []

    #Initialize lxml parser
    page = html.fromstring(page_source)

    #Find start of link
    url_list.extend(page.xpath('//a/@href'))
    url_list.extend(page.xpath('//link/@href'))

    url_list = format_url_list(url_list)

    return url_list


def format_url_list(url_list):
    #Init globals
    global domain

    #Delete doubles from list
    url_list = delete_doubles_from_list(url_list)
    new_url_list = []

    if not domain.endswith("/"):
        domain += "/"

    #Find all valid relative links
    for url in url_list:

        url = url.strip()

        if "." in url or "?" in url:
            continue

        if len(url) < 3:
            continue

        if url.startswith("#"):
            continue

        if url.startswith("//"):
            continue

        if "#" in url:
            index = url.find("#")
            url = url[:index]

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

                if q_len >= constants.THREADS or available == 0:

                    #Get list for multi-thread check
                    new_list = get_list_queue()

                    #Get multi requests
                    result_array = request.multi_request(new_list)

                    #Add to url_dict
                    url_dict = add_to_dict(result_array, url_dict)

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
