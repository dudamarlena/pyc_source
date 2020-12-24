# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\scraper\requests\action\tracer.py
# Compiled at: 2019-03-31 03:23:56
# Size of source mod 2**32: 727 bytes
from collections import UserList, namedtuple
from requests import Response
Visited = namedtuple('Visited', 'url name')

class Tracer(UserList):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    def push(self, url):
        self.append()


def set_tracer(response):
    if not hasattr(response, 'tracer'):
        setattr(response, 'tracer', [])
    response.tracer.insert(0, response.url)