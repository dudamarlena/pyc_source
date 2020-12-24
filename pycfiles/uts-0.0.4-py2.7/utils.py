# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/uts/utils.py
# Compiled at: 2016-10-31 00:57:48
import numpy as np
from collections import Counter

def cosine_sim(c1, c2):
    try:
        n1 = np.sqrt(sum([ x * x for x in list(c1.values()) ]))
        n2 = np.sqrt(sum([ x * x for x in list(c2.values()) ]))
        num = sum([ c1[key] * c2[key] for key in c1 ])
    except:
        assert len(c1) == len(c2)
        n1 = np.sqrt(sum([ x * x for x in c1 ]))
        n2 = np.sqrt(sum([ x * x for x in c2 ]))
        num = sum([ c1[i] * c2[i] for i in range(len(c1)) ])

    try:
        if n1 * n2 < 1e-09:
            return 0
        else:
            return num / (n1 * n2)

    except:
        return 0


class EnglishTokenizer:
    """
    A tokenizer is a class with tokenize(text) method
    """

    def __init__(self):
        pass

    def tokenize(self, text):
        return text.lower().split()