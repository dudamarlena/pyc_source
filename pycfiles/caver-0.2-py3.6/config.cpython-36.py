# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/config.py
# Compiled at: 2018-12-03 22:41:49
# Size of source mod 2**32: 1573 bytes
import os

class Config:
    __doc__ = '\n    Basic config. All model config should inherit this.\n    '
    index_path = os.path.join(os.path.abspath(os.path.curdir), 'caver_index')
    word2index = os.path.join(index_path, 'word2index.json')
    label2index = os.path.join(index_path, 'label2index.json')
    embedding_dim = 256
    sentence_length = 64
    min_word_count = 5
    min_label_count = 100
    valid = 0.15
    batch_size = 256
    epoches = 10
    valid_interval = 200
    recall_k = 5
    cut_model = None
    save_path = 'checkpoint'
    vocab_size = None
    label_num = None
    embedding_file = None
    embedding_train = True
    loss_func = None
    optimizer = None
    drop = 0.15


class ConfigCNN(Config):
    filter_num = 64
    filter_size = [2, 3, 4]


class ConfigSWEN(Config):
    window = 3
    embedding_drop = 0.2


class ConfigLSTM(Config):
    hidden_dim = 128
    layer_num = 1
    bidirectional = False


class ConfigHAN(Config):
    hidden_dim = 64
    layer_num = 1
    bidirectional = True