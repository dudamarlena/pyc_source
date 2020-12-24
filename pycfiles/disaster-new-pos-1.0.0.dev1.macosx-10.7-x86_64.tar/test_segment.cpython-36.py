# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bai/anaconda3/lib/python3.6/site-packages/test/test_segment.py
# Compiled at: 2018-04-13 02:00:45
# Size of source mod 2**32: 1177 bytes
from __future__ import unicode_literals
import codecs, jieba
from news_seg import segmenter

def seg_data(filename):
    """分词方法"""
    words = []
    with filename as (ip):
        for text in ip:
            seg = segmenter.seg(text)
            words.append(seg)

    return words