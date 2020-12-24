# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/metrics/entropy/entropy.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1765 bytes
import javalang
from typing import List
import numpy as np
from scipy.stats import entropy

class Entropy:

    def __init__(self):
        pass

    def __file_to_tokens(self, filename: str) -> List[str]:
        """Takes path to java class file and returns tokens"""
        with open(filename, encoding='utf-8') as (file):
            tokens = javalang.tokenizer.tokenize(file.read())
        return list(map(lambda v: v.value, tokens))

    def value(self, filename: str):
        tokens = self._Entropy__file_to_tokens(filename)
        values, counts = np.unique(tokens, return_counts=True)
        return entropy(counts)