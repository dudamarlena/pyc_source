# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lapis-hong/Documents/Sina/Project/xinci/xinci/selector.py
# Compiled at: 2018-06-18 08:45:11
"""This module generate all possible candidate chinese words."""
from __future__ import unicode_literals
from six.moves import xrange

class CnTextSelector:

    def __init__(self, document, min_len=2, max_len=5):
        """
        Args:
            document: String, filtered chinese corpus.
            min_len: candidate word min length.
            max_len: candidate word max length.
        """
        self._document = document
        self._max_len = max_len
        self._min_len = min_len
        self._doc_len = len(document)

    def generate(self):
        """Returns:
            A generator of candidate chinese word from document.
        """
        for pos in xrange(self._doc_len - self._min_len):
            for cur_len in xrange(self._min_len, self._max_len + 1):
                yield (
                 pos, self._document[pos:pos + cur_len])