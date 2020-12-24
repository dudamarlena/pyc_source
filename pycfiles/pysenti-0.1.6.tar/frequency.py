# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/frequency.py
# Compiled at: 2019-09-20 04:43:26


class BaseProb(object):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 0

    def exists(self, key):
        return key in self.d

    def getsum(self):
        return self.total

    def get(self, key):
        if not self.exists(key):
            return (False, self.none)
        return (
         True, self.d[key])

    def freq(self, key):
        return float(self.get(key)[1]) / self.total

    def samples(self):
        return self.d.keys()


class AddOneProb(BaseProb):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 1

    def add(self, key, value):
        self.total += value
        if not self.exists(key):
            self.d[key] = 1
            self.total += 1
        self.d[key] += value