# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: craigslist/utils.py
# Compiled at: 2019-09-13 10:09:40
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
ALL_SITES_URL = 'http://www.craigslist.org/about/sites'
SITE_URL = 'http://%s.craigslist.org'

def bs(content):
    return BeautifulSoup(content, 'html.parser')


def requests_get(*args, **kwargs):
    """
    Retries if a RequestException is raised (could be a connection error or
    a timeout).
    """
    logger = kwargs.pop('logger', None)
    try:
        return requests.get(*args, **kwargs)
    except RequestException as exc:
        if logger:
            logger.warning('Request failed (%s). Retrying ...', exc)
        return requests.get(*args, **kwargs)

    return


def get_all_sites():
    response = requests.get(ALL_SITES_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    sites = set()
    for box in soup.findAll('div', {'class': 'box'}):
        for a in box.findAll('a'):
            site = a.attrs['href'].rsplit('//', 1)[1].split('.')[0]
            sites.add(site)

    return sites


def get_all_areas(site):
    response = requests.get(SITE_URL % site)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    raw = soup.select('ul.sublinks li a')
    sites = set(a.attrs['href'].rsplit('/')[1] for a in raw)
    return sites


def get_list_filters(url):
    list_filters = {}
    response = requests_get(url)
    soup = bs(response.content)
    for list_filter in soup.find_all('div', class_='search-attribute'):
        filter_key = list_filter.attrs['data-attr']
        filter_labels = list_filter.find_all('label')
        options = [ opt.text.strip() for opt in filter_labels ]
        list_filters[filter_key] = {'url_key': filter_key, 'value': options}

    return list_filters