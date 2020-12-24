# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/goodreads_quotes/__init__.py
# Compiled at: 2015-11-17 04:51:39
# Size of source mod 2**32: 2484 bytes
"""
    goodreads_quotes
    ~~~~~~~~~~~~~~~~

    goodreads_quotes module
"""
import requests
from requests.exceptions import RequestException, Timeout
from lxml import html
from six import u
import json
__version__ = '0.1.0'

class GoodreadsException(Exception):
    __doc__ = 'Goodreads exception\n    '

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        """ Try to pretty-print the exception, if this is going on screen. """

        def red(words):
            return u('\x1b[31m\x1b[49m%s\x1b[0m') % words

        def blue(words):
            return u('\x1b[34m\x1b[49m%s\x1b[0m') % words

        msg = '\n{red_error}\n\n{message}\n'.format(red_error=red('Error occured'), message=blue(str(self.msg)))
        return msg


class Goodreads:

    @staticmethod
    def get_daily_quote():
        try:
            quotes_page = requests.get('https://www.goodreads.com/quotes')
        except Timeout as e:
            raise GoodreadsException(e)
        except RequestException as e:
            raise GoodreadsException(e)

        tree = html.fromstring(quotes_page.content)
        quote_text = tree.xpath('//div[@id="quoteoftheday"]/div[1]/i/text()')[0]
        author = tree.xpath('//div[@id="quoteoftheday"]/div[2]/strong/div/a/text()')[0]
        quote = {'quote': quote_text, 
         'author': author}
        return quote

    @staticmethod
    def get_popular_quotes():
        try:
            quotes_page = requests.get('https://www.goodreads.com/quotes')
        except Timeout as e:
            raise GoodreadsException(e)
        except RequestException as e:
            raise GoodreadsException(e)

        tree = html.fromstring(quotes_page.content)
        quotes = []
        for quote_div in tree.xpath('//div[@class="quoteText"]'):
            quote_text = quote_div.xpath('text()')[0].strip().replace('“', '').replace('”', '')
            author = quote_div.xpath('a/text()')[0].strip()
            quote = {'quote': quote_text, 
             'author': author}
            quotes.append(quote)

        return quotes

    @staticmethod
    def get_daily_quote_as_json():
        return json.dumps(Goodreads.get_daily_quote())

    @staticmethod
    def get_popular_quotes_as_json():
        return json.dumps(Goodreads.get_popular_quotes())