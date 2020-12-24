# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snowpenguin/nagmail/common.py
# Compiled at: 2015-07-20 12:21:43
# Size of source mod 2**32: 769 bytes
from abc import ABCMeta, abstractmethod

class MailQueueDataFetchError(Exception):

    def __init__(self, msg):
        super(MailQueueDataFetchError, self).__init__(msg)


class MailQueueInterface(metaclass=ABCMeta):

    def __init__(self, data_generator):
        self.data_generator = data_generator

    @abstractmethod
    def has_deferred_counter(self):
        pass

    @abstractmethod
    def get_deferred_counter(self):
        pass

    @abstractmethod
    def has_active_counter(self):
        pass

    @abstractmethod
    def get_active_counter(self):
        pass

    @abstractmethod
    def has_total_counter(self):
        pass

    @abstractmethod
    def get_total_counter(self):
        pass

    @abstractmethod
    def update(self):
        pass