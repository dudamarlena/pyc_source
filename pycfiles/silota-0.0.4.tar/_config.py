# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ganesh/work/silota-python/silota/_config.py
# Compiled at: 2013-12-02 21:22:17


class Config(object):

    def __init__(self):
        super(Config, self).__init__()
        self.root_uri = 'https://api.silota.com'
        self.search_root_uri = 'https://search-sandbox.silota.com'
        self.version = 'v1'

    @property
    def uri(self):
        return '%s/%s' % (self.root_uri, self.version)

    @property
    def search_uri(self):
        return '%s/%s' % (self.search_root_uri, self.version)