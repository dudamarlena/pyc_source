# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/classifiers/random.py
# Compiled at: 2018-04-08 14:24:40
# Size of source mod 2**32: 522 bytes
""" Ce module contient toutes les fonctions nécessaires pour implémenter un
classifieur aléatoire
"""
import numpy as np

class Random:

    def __init__(self):
        pass

    def fit(self, datax, datay):
        self.all_labels = np.array(list(set(datay)))

    def predict(self, datax):
        return np.random.choice(self.all_labels)

    def score(self, datax, datay):
        return (self.predict(datax) == datay).mean()


if __name__ == '__main__':
    pass