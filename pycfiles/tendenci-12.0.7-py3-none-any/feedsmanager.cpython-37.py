# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/rss/feedsmanager.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 929 bytes
from datetime import datetime
from django.contrib.syndication.views import Feed
from django.conf import settings

class SubFeed(Feed):

    def __init__(self):
        super(SubFeed, self).__init__()
        self.__qualname__ = self.__class__.__name__

    def items(self):
        return []

    def item_title(self, item):
        return ''

    def item_description(self, item):
        return ''

    def item_link(self, item):
        return ''

    def item_author_name(self, item):
        return ''

    def item_pubdate(self, item):
        return datetime.now()


_feeds_cache = []

def get_all_feeds():
    for app in settings.INSTALLED_APPS:
        _try_import(app + '.feeds')

    return SubFeed.__subclasses__()


def _try_import(module):
    try:
        __import__(module)
    except ImportError:
        pass