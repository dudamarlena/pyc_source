# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/pubsub.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import redis, logging
from threading import Thread
from six.moves.queue import Queue, Full

class QueuedPublisherService(object):
    """
    A publisher that queues items locally and publishes them to a
    remote pubsub service on a background thread.

    Maintains a lossy internal queue for posting, will discard the
    value if the queue is full or not immediately available. Will also
    drop items if the publish operation to the remote service fails.
    """

    def __init__(self, publisher):
        self._started = False
        self.publisher = publisher

    def _start(self):
        if self._started:
            return True
        self.q = q = Queue(maxsize=100)

        def worker():
            while True:
                channel, key, value = q.get()
                try:
                    try:
                        self.publisher.publish(channel, key=key, value=value)
                    except Exception as e:
                        logger = logging.getLogger('sentry.errors')
                        logger.debug('could not submit event to pubsub: %s' % e)

                finally:
                    q.task_done()

        t = Thread(target=worker)
        t.setDaemon(True)
        t.start()
        self._started = True
        return True

    def publish(self, channel, value, key=None):
        if not self._start():
            return
        try:
            self.q.put((channel, key, value), block=False)
        except Full:
            return


class RedisPublisher(object):

    def __init__(self, connection):
        self.rds = None if connection is None else redis.StrictRedis(**connection)
        return

    def publish(self, channel, value, key=None):
        if self.rds is not None:
            self.rds.publish(channel, value)
        return


class KafkaPublisher(object):

    def __init__(self, connection, asynchronous=True):
        from confluent_kafka import Producer
        self.producer = Producer(connection or {})
        self.asynchronous = asynchronous

    def publish(self, channel, value, key=None):
        self.producer.produce(topic=channel, value=value, key=key)
        if not self.asynchronous:
            self.producer.flush()