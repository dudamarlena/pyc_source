# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nn_wtf/data_sets.py
# Compiled at: 2016-12-17 04:58:38
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

class DataSets:

    def __init__(self, train, validation, test):
        self.train = train
        self.validation = validation
        self.test = test