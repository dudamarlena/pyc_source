# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/text_process/preprocess.py
# Compiled at: 2019-10-31 06:52:53
# Size of source mod 2**32: 1713 bytes
from typing import List, Union, Tuple
import tensorflow as tf, numpy as np
from tokenizer_tools.tagset.converter.offset_to_biluo import offset_to_biluo
from tokenizer_tools.tagset.offset.sequence import Sequence
from seq2annotation.input import Lookuper

def str_to_id(string: Union[(str, List[str])], vocabulary_look_table: Lookuper) -> List[int]:
    id_list = [vocabulary_look_table.lookup(i) for i in string]
    return id_list


def id_to_str(id_list: List[int], vocabulary_look_table: Lookuper) -> List[str]:
    str_list = [vocabulary_look_table.inverse_lookup(id) for id in id_list]
    return str_list


def preprocess(data: List[Sequence], tag_lookup_table: Lookuper, vocabulary_look_table: Lookuper, seq_maxlen: Union[(None, int)]=None) -> Tuple[(np.ndarray, np.ndarray, int)]:
    raw_x = []
    raw_y = []
    for offset_data in data:
        tags = offset_to_biluo(offset_data)
        words = offset_data.text
        tag_ids = [tag_lookup_table.lookup(i) for i in tags]
        word_ids = [vocabulary_look_table.lookup(i) for i in words]
        raw_x.append(word_ids)
        raw_y.append(tag_ids)

    if not seq_maxlen:
        seq_maxlen = max(len(s) for s in raw_x)
    print('>>> maxlen: {}'.format(seq_maxlen))
    x = tf.keras.preprocessing.sequence.pad_sequences(raw_x,
      seq_maxlen, padding='post')
    y = tf.keras.preprocessing.sequence.pad_sequences(raw_y,
      seq_maxlen, value=0, padding='post')
    return (
     x, y, seq_maxlen)