# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: craigslist/sites.py
# Compiled at: 2019-02-22 19:44:37
from bs4 import BeautifulSoup
import requests
ALL_SITES_URL = 'http://www.craigslist.org/about/sites'
SITE_URL = 'http://%s.craigslist.org'

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