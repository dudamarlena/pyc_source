# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/btp/util/req.py
# Compiled at: 2017-11-04 01:37:19
# Size of source mod 2**32: 201 bytes


def build_proxies(proxy=None):
    if proxy:
        return {'http':proxy, 
         'https':proxy}