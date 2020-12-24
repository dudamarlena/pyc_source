# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils.py
# Compiled at: 2014-06-16 23:48:32
import bs4

def scrap_scrapme(html):
    soup = bs4.BeautifulSoup(html)
    return soup.find('p').text


def scrap_scrapmepages(html):
    soup = bs4.BeautifulSoup(html)
    return [soup.find('p').text]


def scrap_url(html):
    soup = bs4.BeautifulSoup(html)
    r = soup.find('a')
    return 'http://127.0.0.1:8080' + r['href']


def scrap_allurl(html):
    soup = bs4.BeautifulSoup(html)
    r = soup.findAll('a')
    r = [ 'http://127.0.0.1:8080' + x['href'] for x in r ]
    r = list(set(r))
    return r