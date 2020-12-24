# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/storage/storage.py
# Compiled at: 2015-11-28 05:42:56
# Size of source mod 2**32: 385 bytes


class Storage:

    def __init__(self, f):
        raise Exception('This is an interface')

    def __getitem__(self, key):
        raise Exception('This is an interface')

    def __setitem__(self, key, value):
        raise Exception('This is an interface')

    def __contains__(self, key):
        raise Exception('This is an interface')

    def sync(self):
        raise Exception('This is an interface')