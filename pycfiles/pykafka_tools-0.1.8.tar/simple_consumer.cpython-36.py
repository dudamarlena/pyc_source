# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/rdkafka/simple_consumer.py
# Compiled at: 2018-05-29 17:13:25
# Size of source mod 2**32: 12755 bytes
from contextlib import contextmanager
import logging
from pkg_resources import parse_version
import sys, time
from pykafka.exceptions import RdKafkaStoppedException, ConsumerStoppedException
from pykafka.simpleconsumer import SimpleConsumer, OffsetType
from pykafka.utils.compat import get_bytes
from pykafka.utils.error_handlers import valid_int
from . import _rd_kafka
from . import helpers
log = logging.getLogger(__name__)

class RdKafkaSimpleConsumer(SimpleConsumer):
    """RdKafkaSimpleConsumer"""

    def __init__(self, topic, cluster, consumer_group=None, partitions=None, fetch_message_max_bytes=1048576, num_consumer_fetchers=1, auto_commit_enable=False, auto_commit_interval_ms=60000, queued_max_messages=100000, fetch_min_bytes=1, fetch_error_backoff_ms=500, fetch_wait_max_ms=100, offsets_channel_backoff_ms=1000, offsets_commit_max_retries=5, auto_offset_reset=OffsetType.EARLIEST, consumer_timeout_ms=-1, auto_start=True, reset_offset_on_start=False, compacted_topic=False, generation_id=-1, consumer_id='', deserializer=None, reset_offset_on_fetch=True):
        callargs = {k:v for k, v in vars().items() if k not in ('self', '__class__') if k not in ('self',
                                                                                                  '__class__')}
        self._rdk_consumer = None
        self._poller_thread = None
        self._stop_poller_thread = cluster.handler.Event()
        self._broker_version = cluster._broker_version
        self._fetch_error_backoff_ms = valid_int(fetch_error_backoff_ms)
        (super(RdKafkaSimpleConsumer, self).__init__)(**callargs)

    def _setup_fetch_workers(self):
        brokers = ','.join(b.host + ':' + get_bytes(str(b.port)) for b in self._cluster.brokers.values())
        partition_ids = list(self._partitions_by_id.keys())
        start_offsets = [self._partitions_by_id[p].next_offset for p in partition_ids]
        conf, topic_conf = self._mk_rdkafka_config_lists()
        self._rdk_consumer = _rd_kafka.Consumer()
        log.debug('Configuring _rdk_consumer...')
        self._rdk_consumer.configure(conf=conf)
        self._rdk_consumer.configure(topic_conf=topic_conf)
        start_kwargs = {'brokers':brokers, 
         'topic_name':self._topic.name, 
         'partition_ids':partition_ids, 
         'start_offsets':start_offsets}
        log.debug('Starting _rdk_consumer with {}'.format(start_kwargs))
        (self._rdk_consumer.start)(**start_kwargs)

        def poll(rdk_handle, stop_event):
            while not stop_event.is_set():
                try:
                    rdk_handle.poll(timeout_ms=1000)
                except RdKafkaStoppedException:
                    break
                except:
                    self._worker_exception = sys.exc_info()

            log.debug('Exiting RdKafkaSimpleConsumer poller thread cleanly.')

        self._stop_poller_thread.clear()
        self._poller_thread = self._cluster.handler.spawn(poll,
          args=(self._rdk_consumer, self._stop_poller_thread))

    def consume(self, block=True, unblock_event=None):
        timeout_ms = self._consumer_timeout_ms if block else 1
        try:
            msg = self._consume(timeout_ms, unblock_event)
        except (RdKafkaStoppedException, AttributeError) as e:
            if not self._running:
                raise ConsumerStoppedException
            else:
                raise
        else:
            if not self._running:
                raise ConsumerStoppedException
            if msg is not None:
                self._partitions_by_id[msg.partition_id].set_offset(msg.offset)
            return msg

    def _consume(self, timeout_ms, unblock_event):
        """Helper to allow catching interrupts around rd_kafka_consume"""
        inner_timeout_ms = 500
        if timeout_ms < 0:
            while True:
                self._raise_worker_exceptions()
                if unblock_event:
                    if unblock_event.is_set():
                        return
                else:
                    msg = self._rdk_consumer.consume(inner_timeout_ms)
                    if msg is not None:
                        return msg

        else:
            t_start = time.time()
            leftover_ms = timeout_ms
            while leftover_ms > 0:
                self._raise_worker_exceptions()
                if unblock_event:
                    if unblock_event.is_set():
                        return
                inner_timeout_ms = int(min(leftover_ms, inner_timeout_ms))
                msg = self._rdk_consumer.consume(inner_timeout_ms)
                if msg is not None:
                    return msg
                elapsed_ms = 1000 * (time.time() - t_start)
                leftover_ms = timeout_ms - elapsed_ms

    def stop(self):
        ret = super(RdKafkaSimpleConsumer, self).stop()
        if self._rdk_consumer is not None:
            self._stop_poller_thread.set()
            self._rdk_consumer.stop()
            log.debug('Issued stop to _rdk_consumer.')
            self._rdk_consumer = None
        return ret

    def fetch_offsets(self):
        with self._stop_start_rdk_consumer():
            return super(RdKafkaSimpleConsumer, self).fetch_offsets()

    def reset_offsets(self, partition_offsets=None):
        with self._stop_start_rdk_consumer():
            return super(RdKafkaSimpleConsumer, self).reset_offsets(partition_offsets)

    @contextmanager
    def _stop_start_rdk_consumer(self):
        """Context manager for methods to temporarily stop _rdk_consumer

        We need this because we hold read-offsets both in pykafka and
        internally in _rdk_consumer.  We'll hold the one in pykafka to be the
        ultimate source of truth.  So whenever offsets are to be changed (other
        than through consume() that is), we need to clobber _rdk_consumer.
        """
        restart_required = self._running and self._rdk_consumer is not None
        if restart_required:
            self._rdk_consumer.stop()
            log.debug('Temporarily stopped _rdk_consumer.')
        yield
        if restart_required:
            self._setup_fetch_workers()
            log.debug('Restarted _rdk_consumer.')

    def _mk_rdkafka_config_lists(self):
        """Populate conf, topic_conf to configure the rdkafka consumer"""
        ver10 = parse_version(self._broker_version) >= parse_version('0.10.0')
        conf = {'client.id':'pykafka.rdkafka', 
         'receive.message.max.bytes':self._fetch_message_max_bytes * len(self.partitions) + 1, 
         'socket.timeout.ms':self._cluster._socket_timeout_ms, 
         'queued.min.messages':self._queued_max_messages, 
         'queued.max.messages.kbytes':str(self._queued_max_messages * self._fetch_message_max_bytes // 1024), 
         'fetch.wait.max.ms':self._fetch_wait_max_ms, 
         'fetch.message.max.bytes':self._fetch_message_max_bytes, 
         'fetch.min.bytes':self._fetch_min_bytes, 
         'fetch.error.backoff.ms':self._fetch_error_backoff_ms, 
         'api.version.request':ver10}
        if not ver10:
            conf['broker.version.fallback'] = self._broker_version
        conf.update(helpers.rdk_ssl_config(self._cluster))
        map_offset_types = {OffsetType.EARLIEST: 'smallest', 
         OffsetType.LATEST: 'largest'}
        topic_conf = {'auto.commit.enable':'false', 
         'auto.offset.reset':map_offset_types[self._auto_offset_reset]}
        conf = [(key, str(conf[key])) for key in conf]
        topic_conf = [(key, str(topic_conf[key])) for key in topic_conf]
        return (
         conf, topic_conf)