# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/onema/Code/python/evee/build/lib/evee/abstract_event_subscriber.py
# Compiled at: 2016-03-13 16:31:26
# Size of source mod 2**32: 200 bytes
from abc import ABCMeta
from abc import abstractmethod

class AbstractEventSubscriber(object, metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def get_subscribed_events():
        pass