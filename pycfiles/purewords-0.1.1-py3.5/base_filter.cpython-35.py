# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/base_filter.py
# Compiled at: 2018-08-07 00:28:11
# Size of source mod 2**32: 145 bytes
"""base filter"""
from abc import abstractmethod

class BaseFilter(object):

    @abstractmethod
    def __call__(self, sentence):
        pass