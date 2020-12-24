# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils_test.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 145 bytes
from parser_engine.utils import *
if __name__ == '__main__':
    p = closest_parser_engine_json('.json')
    if not p == '':
        raise AssertionError