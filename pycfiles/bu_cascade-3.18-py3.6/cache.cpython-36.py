# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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