# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/get_podcasts.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 337 bytes
from hoerapi.lowlevel import call_api
from hoerapi.util import CommonEqualityMixin
from hoerapi.parser import parser_list

class Podcast(CommonEqualityMixin):

    def __init__(self, data):
        self.slug = data['slug']
        self.title = data['title']


def get_podcasts():
    return parser_list(Podcast, call_api('getPodcasts'))