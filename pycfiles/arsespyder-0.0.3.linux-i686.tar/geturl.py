# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pyarsespyder/geturl.py
# Compiled at: 2013-09-22 14:18:23
from urllib2 import build_opener, URLError, HTTPError
from bs4 import BeautifulSoup as Soup

def url_to_string(url):
    """ 
    This functions returns the text of the page specified by url parameter
   
    Keyword arguments:
    url -- a URL whose text will be returned

    """
    try:
        opened = build_opener()
        string = opened.open(url).read()
    except (URLError, HTTPError, ValueError):
        return ''

    return string


def get_url_list(html_text):
    """ 
    This functions returns a list with all the links of type
    <a href="http://whatever">whatever</a> contained
   
    Keyword arguments:
    html_text -- HTML text where <a href="http://whatever">whatever</a>
                 links will be searched

    """
    text = url_to_string(html_text)
    try:
        s = Soup(text)
        return [ x['href'] for x in s.findAll('a', href=True) ]
    except:
        print 'ERROR ON SOUP CREATION'
        return []