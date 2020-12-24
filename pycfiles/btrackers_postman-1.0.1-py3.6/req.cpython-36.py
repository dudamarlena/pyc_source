# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/btp/util/req.py
# Compiled at: 2017-11-04 01:37:19
# Size of source mod 2**32: 201 bytes


def build_proxies(proxy=None):
    if proxy:
        return {'http':proxy,  'https':proxy}