# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bpiwowar/development/datasets/datasets/warc.py
# Compiled at: 2016-11-18 05:08:00
# Size of source mod 2**32: 147 bytes
from . import data

class Handler(data.Documents):

    def __init__(self, context, config):
        data.Documents.__init__(self, context, config)