# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/padding.py
# Compiled at: 2020-03-19 03:31:58
# Size of source mod 2**32: 601 bytes
import torch

def sents2t(sentences, seq_len, default=0):
    ret = torch.ones((len(sentences)), seq_len, dtype=(torch.int64)) * default
    for _id, sentence in enumerate(sentences):
        ret[_id, 0:len(sentence)] = torch.tensor(sentence, dtype=(torch.int64))

    return ret


def b_sents2t(batch, seq_len, default=0):
    ret = torch.ones((len(batch)), (len(batch[0])), seq_len, dtype=(torch.int64)) * default
    for bid, sentences in enumerate(batch):
        for sid, sentence in enumerate(sentences):
            ret[bid, sid, 0:len(sentence)] = torch.tensor(sentence, dtype=(torch.int64))

    return ret