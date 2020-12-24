# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\publishsubscribe\Subscriber.py
# Compiled at: 2018-01-18 12:33:20
# Size of source mod 2**32: 2262 bytes
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Subscriber(object):

    def _data_added(self, publisher, id_, item):
        """
        Notification received from a Publisher when data has been added.
        Subclasses of Subscriber should override this.

        :param expatriate.publishsubscribe.Publisher publisher: The publishing object
        :param id_: The added id. Can be index for a list or key for a dict.
        :param item: The added item.
        """
        pass

    def _data_updated(self, publisher, id_, old_item, new_item):
        """
        Notification received from a Publisher when data has been updated.
        Subclasses of Subscriber should override this.

        :param expatriate.publishsubscribe.Publisher publisher: The publishing object
        :param id_: The updated id. Can be index for a list or key for a dict.
        :param old_item: The old item, before the update.
        :param new_item: The new item, after the update.
        """
        pass

    def _data_deleted(self, publisher, id_, item):
        """
        Notification received from a Publisher when data has been deleted.
        Subclasses of Subscriber should override this.

        :param expatriate.publishsubscribe.Publisher publisher: The publishing object
        :param id_: The deleted ids. Can be index for a list or key for a dict.
        :param item: The deleted item.
        """
        pass