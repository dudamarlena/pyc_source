# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lapis-hong/Documents/Sina/Project/new-words-finder/xinci/new_words_finder.py
# Compiled at: 2018-06-18 01:04:11
from xinci.algorithm import EntropyJudger
from xinci.dictionary import Dictionary
from xinci.selector import CnTextSelector

class NewWordFinder:

    def __init__(self, min_candidate_len=2, max_candidate_len=6, least_cnt_threshold=1, solid_rate_threshold=0.018, entropy_threshold=1.92):
        self._min_candidate_len = min_candidate_len
        self._max_candidate_len = max_candidate_len
        self._least_cnt_threshold = least_cnt_threshold
        self._solid_rate_threshold = solid_rate_threshold
        self._entropy_threshold = entropy_threshold
        self.dictionary = Dictionary()

    stopwords = {
     '我', '你', '您', '他', '她', '谁', '哪', '那', '这',
     '的', '了', '着', '也', '是', '有', '不', '在', '与',
     '呢', '啊', '呀', '吧', '嗯', '哦', '哈', '呐'}

    def find(self, document):
        """New word discover is based on statistic and entropy, better to sure
        document size is in 100kb level, or you may get a unsatisfied result.
        """
        new_word_set = set()
        selector = CnTextSelector(document, self._min_candidate_len, self._max_candidate_len)
        judger = EntropyJudger(document, self._least_cnt_threshold, self._solid_rate_threshold, self._entropy_threshold)
        while not selector.end():
            candidate = selector.next()
            if not candidate:
                continue
            if candidate[0] in self.stopwords or candidate[(-1)] in self.stopwords:
                continue
            if candidate in self.dictionary or candidate in new_word_set:
                continue
            print candidate
            if judger.judge(candidate):
                new_word_set.add(candidate)

        return new_word_set


if __name__ == '__main__':
    from xinci.utils import data_reader
    document = data_reader('test.txt')
    new_word_finder = NewWordFinder()
    new_words = new_word_finder.find(document)
    print new_words