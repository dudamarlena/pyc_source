# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen_plugins/nlp_model_gen_plugins/utils/collectionsUtils.py
# Compiled at: 2019-06-14 18:08:06
# Size of source mod 2**32: 251 bytes
from collections import Counter

def tuple_word_list_to_counter(tuple_list):
    counter = Counter()
    if not tuple_list:
        return counter
    else:
        for word, count in tuple_list:
            counter[word.lower()] += count

        return counter