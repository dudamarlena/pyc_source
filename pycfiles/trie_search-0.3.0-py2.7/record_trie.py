# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/trie_search/record_trie.py
# Compiled at: 2018-01-16 00:05:32
from marisa_trie import RecordTrie
from .trie import TrieSearch

class RecordTrieSearch(RecordTrie, TrieSearch):

    def __init__(self, record_format, records=None, filepath=None, splitter=' '):
        super(RecordTrieSearch, self).__init__(record_format, records)
        self.splitter = splitter
        if filepath:
            self.load(filepath)

    def search_all_patterns(self, text, min_weight=0.0):
        for pattern, start_idx in super(RecordTrie, self).search_all_patterns(text):
            weight = self[pattern][0][0]
            if weight < min_weight:
                continue
            yield (
             pattern, start_idx, weight)

    def search_longest_patterns(self, text, min_weight=0.0):
        all_patterns = self.search_all_patterns(text, min_weight)
        check_field = [0] * len(text)
        for pattern, start_idx, weight in sorted(all_patterns, key=lambda x: len(x[0]), reverse=True):
            target_field = check_field[start_idx:start_idx + len(pattern)]
            check_sum = sum(target_field)
            if check_sum == 0:
                for i in range(len(pattern)):
                    check_field[start_idx + i] = 1

                yield (
                 pattern, start_idx, weight)