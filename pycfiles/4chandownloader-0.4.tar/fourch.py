# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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