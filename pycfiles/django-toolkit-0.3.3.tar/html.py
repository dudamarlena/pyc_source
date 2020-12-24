# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/ahayes/data/.workspaces/juno/django-toolkit/django_toolkit/markup/html.py
# Compiled at: 2013-03-19 00:20:36
from bs4 import BeautifulSoup

def get_anchor_href(markup):
    """
    Given HTML markup, return a list of hrefs for each anchor tag.
    """
    soup = BeautifulSoup(markup, 'lxml')
    return [ '%s' % link.get('href') for link in soup.find_all('a') ]


def get_anchor_contents(markup):
    """
    Given HTML markup, return a list of href inner html for each anchor tag.
    """
    soup = BeautifulSoup(markup, 'lxml')
    return [ '%s' % link.contents[0] for link in soup.find_all('a') ]