# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zed/venvs/4ch/lib/python2.7/site-packages/fourch/fourch.py
# Compiled at: 2014-09-20 10:44:49
from ._version import __version__
urls = {'api': 'a.4cdn.org', 
   'boards': 'boards.4chan.org', 
   'images': 'i.4cdn.org', 
   'thumbs': 't.4cdn.org', 
   'api_board': '/{board}/{page}.json', 
   'api_thread': '/{board}/thread/{thread}.json', 
   'api_threads': '/{board}/threads.json', 
   'api_catalog': '/{board}/catalog.json', 
   'api_boards': '/boards.json'}

class struct:

    def __init__(self, **entries):
        self.__dict__.update(entries)