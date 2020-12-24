# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shershen/workspace/scheduler.git/synergy/db/model/queue_context_entry.py
# Compiled at: 2016-06-29 16:46:55
# Size of source mod 2**32: 1049 bytes
__author__ = 'Bohdan Mushkevych'
from odm.document import BaseDocument
from odm.fields import StringField
MQ_QUEUE = 'mq_queue'
MQ_EXCHANGE = 'mq_exchange'
MQ_ROUTING_KEY = 'mq_routing_key'

class QueueContextEntry(BaseDocument):
    __doc__ = ' Non-persistent model. This class presents Queue Context Entry record '
    mq_queue = StringField(MQ_QUEUE)
    mq_exchange = StringField(MQ_EXCHANGE)
    mq_routing_key = StringField(MQ_ROUTING_KEY)

    @BaseDocument.key.getter
    def key(self):
        return self.mq_queue

    @key.setter
    def key(self, value):
        """ :param value: name of the mq queue """
        self.mq_queue = value


def queue_context_entry(exchange, queue_name, routing=None):
    """ forms queue's context entry """
    if routing is None:
        routing = queue_name
    queue_entry = QueueContextEntry(mq_queue=queue_name, mq_exchange=exchange,
      mq_routing_key=routing)
    return queue_entry