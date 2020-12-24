# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/constants.py
# Compiled at: 2019-11-07 04:44:02
# Size of source mod 2**32: 268 bytes
from enum import Enum

class ExtractType(Enum):
    NEWS = 1
    LIST = 2


class ExtractorType(Enum):
    XPATH = 1
    JSONPATH = 2