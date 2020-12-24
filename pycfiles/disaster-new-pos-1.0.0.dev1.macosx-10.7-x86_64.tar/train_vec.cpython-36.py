# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bai/anaconda3/lib/python3.6/site-packages/vec_model/train_vec.py
# Compiled at: 2018-04-03 02:11:24
# Size of source mod 2**32: 2028 bytes
"""
author: mario
data: 2018/4/2
"""
import jieba, re, numpy as np, multiprocessing, codecs, logging
from gensim.models import KeyedVectors
from gensim.models import word2vec
embed_dim = 128
window_size = 7
min_counts = 3
n_iter = 10
cpu_count = multiprocessing.cpu_count()

def read_file():
    """读文件"""
    train_data = codecs.open('../data/combine_seg_data.txt', 'r', encoding='utf-8')
    train_datas = []
    with train_data as (td):
        for data in td:
            data = data.strip().split()
            train_datas.extend(data)

    train_data.close()
    return train_datas


def word2vec_train():
    """训练词向量"""
    sentences = word2vec.Text8Corpus('../data/combine_seg_data.txt')
    model = word2vec.Word2Vec(sentences, size=embed_dim, sg=1, window=window_size, hs=1, workers=cpu_count, min_count=min_counts)
    model.wv.save_word2vec_format('../vec_model/word2vec_models.txt', binary=0)


def train():
    """训练模型的方法"""
    print('Tokenising...')
    print('Training a Word2vec model...')
    word2vec_train()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=(logging.INFO))
    train()