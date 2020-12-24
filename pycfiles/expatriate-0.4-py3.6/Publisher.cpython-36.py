# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\publishsubscribe\Publisher.py
# Compiled at: 2018-01-18 12:33:12
# Size of source mod 2**32: 2970 bytes
import logging
from .exceptions import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Publisher(object):
    __doc__ = ' Class for a generic data structure that publishes data content changes to a list of subscribers '

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        """
        Add a subscriber of this data structure that receives updates via _data_added, _data_deleted and _data_updated calls.

        :param expatriate.publishsubscribe.Subscriber subscriber: The subscriber that wishes to listen to change events from this publisher.
        :raises SubscriberException: if the *subscriber* does not subclass Subscriber
        """
        from .Subscriber import Subscriber
        if isinstance(subscriber, Subscriber):
            self._subscribers.append(subscriber)
        else:
            raise SubscriberException(str(subscriber) + ' does not inherit from Subscriber')

    def _publish_added(self, id_, item):
        """
        Subclasses should call this method to publish additions to subscribers.

        :param id_: The added id. Can be index for a list or key for a dict.
        :param item: The added item.
        """
        for subscriber in self._subscribers:
            subscriber._data_added(self, id_, item)

    def _publish_updated(self, id_, old_item, new_item):
        """
        Subclasses should call this method to publish updates to subscribers.

        :param id_: The updated id. Can be index for a list or key for a dict.
        :param old_item: The old item, before the update.
        :param new_item: The new item, after the update.
        """
        for subscriber in self._subscribers:
            subscriber._data_updated(self, id_, old_item, new_item)

    def _publish_deleted(self, id_, item):
        """
        Subclasses should call this method to publish deletions to subscribers.

        :param id_: The deleted ids. Can be index for a list or key for a dict.
        :param item: The deleted item.
        """
        for subscriber in self._subscribers:
            subscriber._data_deleted(self, id_, item)