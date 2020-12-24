# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bu_cascade/utilities/cache.py
# Compiled at: 2019-10-30 15:19:36
# Size of source mod 2**32: 252 bytes


class Cache(object):

    def __init__(self):
        self.cache = {}

    def clear_cache(self):
        self.cache = {}

    def retrieve_asset(self):
        pass

    def get_instance(self, service):
        pass