# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZhongLP/segmenter.py
# Compiled at: 2019-12-21 11:02:32
# Size of source mod 2**32: 2821 bytes
"""
Created on Sat Jan 19 18:21:13 2019

@author: limingfan
"""
import jieba, re
from .segmenter_pk.shortest_bigram import ShortestBigramSegmenter

class Segmenter(ShortestBigramSegmenter):
    __doc__ = '\n    '

    def __init__(self):
        super(Segmenter, self).__init__()
        self.reset_patterns()

    def reset_patterns(self):
        """
        """
        self.flag_replace = 0
        self.pattern_int = re.compile('^[0-9]+$')
        self.pattern_float = re.compile('^[0-9,]*\\.[0-9,]+$')
        self.pattern_percent = re.compile('^[\\.0-9,]+%+$')
        self.list_patterns = []
        self.list_patterns.append((self.pattern_int, '[tkn_int]'))
        self.list_patterns.append((self.pattern_float, '[tkn_float]'))
        self.list_patterns.append((self.pattern_percent, '[tkn_percent]'))
        self.pattern_longalnum = re.compile('^[0-9,%\\\\/\\.a-zA-Z]+$')
        self.long_alnum_threshold = 20
        self.list_patterns_length = []
        self.list_patterns_length.append((
         self.pattern_longalnum, '[tkn_alnum]', self.long_alnum_threshold))

    def segment_and_replace(self, text):
        """
        """
        list_before_rep = self.segment(text)
        return self.replace_patterned_tokens(list_before_rep)

    def replace_patterned_tokens(self, list_before_rep):
        """
        """
        list_rep = []
        for token in list_before_rep:
            for pattern, rep_token in self.list_patterns:
                if pattern.match(token):
                    list_rep.append(rep_token)
                    break
            else:
                for pattern, rep_token, thr in self.list_patterns_length:
                    if pattern.match(token):
                        if len(token) >= thr:
                            list_rep.append(rep_token)
                            break
                else:
                    list_rep.append(token)

        return list_rep


if __name__ == '__main__':
    segmenter = Segmenter()
    text = '-2019年1月21日国家统计局发布，2018年中国国内生产总值-90.0309万亿元，按可比价格计算，同比增长6.6%。证书编号：PS20190309。'
    print(text)
    tokens = segmenter.segment(text)
    print(tokens)
    text = '宣紙上走筆至此擱一半'
    print(text)
    tokens = segmenter.segment(text)
    print(tokens)