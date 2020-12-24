# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp3/utils/dfa_filters.py
# Compiled at: 2019-11-08 04:26:21
# Size of source mod 2**32: 1628 bytes
from __future__ import unicode_literals

class DFAFilter:
    __doc__ = '\n    Examples:\n    ::\n        dfa_filter = DFAFilter()\n        dfa_filter.build_chains(keywords_set)\n        dfa_filter.load_keywords(raw_text)\n    '

    def load_keywords(self, raw_text):
        """
        Args:
            raw_text (str):

        Returns:
            set: keywords that in raw_text
        """
        assert getattr(self, '_chains', None), 'Should invoke build_chains first'
        return self.filter_keyword(raw_text)

    def build_chains(self, keywords):
        """
        Args:
            keywords (set): lexicon of keywords
        """
        chains = {}
        for word in keywords:
            node = chains

        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        else:
            self._chains = chains

    def is_word_in_chains(self, chains, raw_text, n_len, i):
        if raw_text[i] not in chains:
            return
        else:
            return chains[raw_text[i]] or i
        if i == n_len - 1:
            return
        return self.is_word_in_chains(chains=(chains[raw_text[i]]),
          raw_text=raw_text,
          n_len=n_len,
          i=(i + 1))

    def filter_keyword(self, raw_text):
        result_keywords = set()
        i, n_len = 0, len(raw_text)
        for i in range(n_len):
            li = self.is_word_in_chains(self._chains, raw_text, n_len, i)
            if li is not None:
                result_keywords.add(raw_text[i:li + 1])
            return result_keywords