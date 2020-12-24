# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lapis-hong/Documents/Sina/Project/new-words-finder/xinci/algorithm.py
# Compiled at: 2018-06-17 23:08:04
from __future__ import unicode_literals
from __future__ import division
import math
from indexer import CnTextIndexer
from utils import WordCountDict

class EntropyJudger:
    """Use entropy and solid rate to judge whether a candidate is a chinese word or not."""

    def __init__(self, document, least_cnt_threshold=5, solid_rate_threshold=0.018, entropy_threshold=1.92):
        """
        Args:
            least_cnt_threshold: a word least appeared count, can not pass judge if less than this value.
            solid_rate_threshold: p(candidate)/p(candidate[0]) * p(candidate)/p(candidate[1]) * ...
            entropy_threshold: min(left_char_entropy, right_char_entropy), The smaller this values is, 
                more new words you will get, but with less accuracy.
        """
        self.least_cnt_threshold = least_cnt_threshold
        self.solid_rate_threshold = solid_rate_threshold
        self.entropy_threshold = entropy_threshold
        self.indexer = CnTextIndexer(document)

    def judge(self, candidate):
        solid_rate = self._get_solid_rate(candidate)
        entropy = self._get_entropy(candidate)
        if solid_rate < self.solid_rate_threshold or entropy < self.entropy_threshold:
            return False
        return True

    def _get_solid_rate(self, candidate):
        if len(candidate) < 2:
            return 1.0
        count = self.indexer.count(candidate)
        if count < self.least_cnt_threshold:
            return 0.0
        rate = 1.0
        for c in candidate:
            rate *= count / self.indexer.count(c)

        return math.pow(rate, 1 / float(len(candidate))) * math.sqrt(len(candidate))

    def _get_entropy(self, candidate):
        left_char_dic = WordCountDict()
        right_char_dic = WordCountDict()
        candidate_pos_generator = self.indexer.find(candidate)
        for pos in candidate_pos_generator:
            c = self.indexer[(pos - 1)]
            left_char_dic.add(c)
            c = self.indexer[(pos + len(candidate))]
            right_char_dic.add(c)

        previous_total_char_cnt = left_char_dic.count()
        next_total_char_cnt = right_char_dic.count()
        previous_entropy = 0.0
        next_entropy = 0.0
        for char, count in left_char_dic.items():
            prob = count / previous_total_char_cnt
            previous_entropy -= prob * math.log(prob)

        for char, count in right_char_dic.items():
            prob = count / next_total_char_cnt
            next_entropy -= prob * math.log(prob)

        return min(previous_entropy, next_entropy)


if __name__ == b'__main__':
    from utils import data_reader
    document = data_reader(b'test.txt')
    jugder = EntropyJudger(document)
    print jugder._get_entropy(b'食物')
    print jugder._get_solid_rate(b'食物')
    print jugder.judge(b'食物')