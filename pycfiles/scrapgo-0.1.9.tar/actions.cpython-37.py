# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\scraper\actions.py
# Compiled at: 2019-03-10 08:32:22
# Size of source mod 2**32: 775 bytes
import re
from collections import namedtuple
Link = namedtuple('Link', 'pattern urlfilter parser name recursive')
Location = namedtuple('Location', 'url parser name')
Source = namedtuple('Source', 'pattern, urlfilter parser name')

def location(url, parser, name=None):
    return Location(url, parser, name or url)


def href(pattern, urlfilter=None, parser=None, name=None, recursive=False):
    regx = re.compile(pattern)
    return Link(regx, urlfilter, parser, name or pattern, recursive)


def src(pattern, urlfilter=None, parser=None, name=None):
    regx = re.compile(pattern)
    return Source(regx, urlfilter, parser, name or pattern)