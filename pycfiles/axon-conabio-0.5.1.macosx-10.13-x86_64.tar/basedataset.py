# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/datasets/basedataset.py
# Compiled at: 2018-12-10 18:39:29
from abc import ABCMeta, abstractmethod
import six

@six.add_metaclass(ABCMeta)
class Dataset(object):

    @abstractmethod
    def iter_train(self):
        pass

    @abstractmethod
    def iter_validation(self):
        pass

    @abstractmethod
    def iter_test(self):
        pass