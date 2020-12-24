# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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