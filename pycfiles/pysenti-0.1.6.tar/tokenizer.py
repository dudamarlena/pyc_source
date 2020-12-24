# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/tokenizer.py
# Compiled at: 2019-09-22 00:23:33
"""
@author:XuMing（xuming624@qq.com)
@description: 配置切词器
"""
import logging, jieba
from jieba import posseg
from .compat import strdecode
jieba.default_logger.setLevel(logging.ERROR)

def segment(sentence, cut_type='word', pos=False):
    u"""
    切词
    :param sentence:
    :param cut_type: 'word' use jieba.lcut; 'char' use list(sentence)
    :param pos: enable POS
    :return: list
    """
    sentence = strdecode(sentence)
    if pos:
        if cut_type == 'word':
            return posseg.lcut(sentence)
        if cut_type == 'char':
            word_seq = list(sentence)
            pos_seq = []
            for w in word_seq:
                w_p = posseg.lcut(w)
                pos_seq.append(w_p[0].flag)

            return (word_seq, pos_seq)
    else:
        if cut_type == 'word':
            return jieba.lcut(sentence)
        if cut_type == 'char':
            return list(sentence)