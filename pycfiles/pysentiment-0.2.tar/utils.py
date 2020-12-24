# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/utils.py
# Compiled at: 2019-09-22 00:12:07
__doc__ = '\n@author:XuMing（xuming624@qq.com)\n@description: \n'
import os, pickle, re
from codecs import open
from pysenti import config

def load_set(path):
    words = set()
    with open(path, 'r', 'utf-8') as (f):
        for line in f:
            words.add(line.strip())

    return words


re_zh = re.compile('([\\u4E00-\\u9FA5]+)')
stopwords = load_set(config.stopwords_path)

def filter_stop(words):
    return list(filter(lambda x: x not in stopwords, words))


def load_pkl(pkl_path):
    u"""
    加载词典文件
    :param pkl_path:
    :return:
    """
    with open(pkl_path, 'rb') as (f):
        result = pickle.load(f)
    return result


def dump_pkl(vocab, pkl_path, overwrite=True):
    u"""
    存储文件
    :param pkl_path:
    :param overwrite:
    :return:
    """
    if pkl_path and os.path.exists(pkl_path) and not overwrite:
        return
    if pkl_path:
        with open(pkl_path, 'wb') as (f):
            pickle.dump(vocab, f, protocol=0)
        print 'save %s ok.' % pkl_path
    else:
        raise IOError('no file: %s' % pkl_path)


def split_sentence(sentence):
    pattern = re.compile('[，。%、！!？?,；～~.… ]+')
    clauses = [ i for i in pattern.split(sentence.strip()) if i ]
    return clauses


if __name__ == '__main__':
    sent = 'nihao,我是警察，你站起来。我要问你话！好不。'
    k = split_sentence(sent)
    print k