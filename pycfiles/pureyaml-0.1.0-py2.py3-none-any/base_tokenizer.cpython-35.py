# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/tokenizer/base_tokenizer.py
# Compiled at: 2018-08-07 00:23:56
# Size of source mod 2**32: 146 bytes
__doc__ = 'base tokenizer'
from abc import abstractmethod

class BaseTokenizer(object):

    @abstractmethod
    def cut(self, sentence):
        pass