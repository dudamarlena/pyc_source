# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/producer.py
# Compiled at: 2018-07-05 13:25:31
# Size of source mod 2**32: 38656 bytes
from __future__ import division
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['Producer']
from collections import deque
import logging, platform, struct, sys, threading, time, weakref
from six import reraise
from .common import CompressionType
from .exceptions import ERROR_CODES, KafkaException, InvalidMessageSize, MessageSizeTooLarge, NotLeaderForPartition, ProduceFailureError, ProducerQueueFullError, ProducerStoppedException, SocketDisconnectedError
from .partitioners import RandomPartitioner
from .protocol import Message, ProduceRequest
from .utils.compat import iteritems, itervalues, Empty
from .utils.error_handlers import valid_int
from .utils import msg_protocol_version
log = logging.getLogger(__name__)

class Producer(object):
    """Producer"""

    def __init__(self, cluster, topic, partitioner=None, compression=CompressionType.NONE, max_retries=3, retry_backoff_ms=100, required_acks=1, ack_timeout_ms=10000, max_queued_messages=100000, min_queued_messages=70000, linger_ms=5000, queue_empty_timeout_ms=0, block_on_queue_full=True, max_request_size=1000012, sync=False, delivery_reports=False, pending_timeout_ms=5000, auto_start=True, serializer=None):
        """Instantiate a new AsyncProducer

        :param cluster: The cluster to which to connect
        :type cluster: :class:`pykafka.cluster.Cluster`
        :param topic: The topic to which to produce messages
        :type topic: :class:`pykafka.topic.Topic`
        :param partitioner: The partitioner to use during message production
        :type partitioner: :class:`pykafka.partitioners.BasePartitioner`
        :param compression: The type of compression to use.
        :type compression: :class:`pykafka.common.CompressionType`
        :param max_retries: How many times to attempt to produce a given batch of
            messages before raising an error. Allowing retries will potentially change
            the ordering of records because if two records are sent to a single partition,
            and the first fails and is retried but the second succeeds, then the second
            record may appear first. If you want to completely disallow message
            reordering, use `sync=True`.
        :type max_retries: int
        :param retry_backoff_ms: The amount of time (in milliseconds) to
            back off during produce request retries. This does not equal the total time
            spent between message send attempts, since that number can be influenced
            by other kwargs, including `linger_ms` and `socket_timeout_ms`.
        :type retry_backoff_ms: int
        :param required_acks: The number of other brokers that must have
            committed the data to their log and acknowledged this to the leader
            before a request is considered complete
        :type required_acks: int
        :param ack_timeout_ms: The amount of time (in milliseconds) to wait for
            acknowledgment of a produce request on the server.
        :type ack_timeout_ms: int
        :param max_queued_messages: The maximum number of messages the producer
            can have waiting to be sent to the broker. If messages are sent
            faster than they can be delivered to the broker, the producer will
            either block or throw an exception based on the preference specified
            with block_on_queue_full.
        :type max_queued_messages: int
        :param min_queued_messages: The minimum number of messages the producer
            can have waiting in a queue before it flushes that queue to its
            broker (must be greater than 0). This paramater can be used to
            control the number of messages sent in one batch during async
            production. This parameter is automatically overridden to 1
            when `sync=True`.
        :type min_queued_messages: int
        :param linger_ms: This setting gives the upper bound on the delay for
            batching: once the producer gets min_queued_messages worth of
            messages for a broker, it will be sent immediately regardless of
            this setting.  However, if we have fewer than this many messages
            accumulated for this partition we will 'linger' for the specified
            time waiting for more records to show up. linger_ms=0 indicates no
            lingering - messages are sent as fast as possible after they are
            `produce()`d.
        :type linger_ms: int
        :param queue_empty_timeout_ms: The amount of time in milliseconds for which
            the producer's worker threads should block when no messages are available
            to flush to brokers. After each `linger_ms` interval, the worker thread
            checks for the presence of at least one message in its queue. If there is
            not at least one, it enters an "empty wait" period for
            `queue_empty_timeout_ms` before starting a new `linger_ms` wait loop. If
            `queue_empty_timeout_ms` is 0, this "empty wait" period is a noop, and
            flushes will continue to be attempted at intervals of `linger_ms`, even
            when the queue is empty. If `queue_empty_timeout_ms` is a positive integer,
            this "empty wait" period will last for at most that long, but it ends earlier
            if a message is `produce()`d before that time. If `queue_empty_timeout_ms` is
            -1, the "empty wait" period can only be stopped (and the worker thread killed)
            by a call to either `produce()` or `stop()` - it will never time out.
        :type queue_empty_timeout_ms: int
        :param block_on_queue_full: When the producer's message queue for a
            broker contains max_queued_messages, we must either stop accepting
            new messages (block) or throw an error. If True, this setting
            indicates we should block until space is available in the queue.
            If False, we should throw an error immediately.
        :type block_on_queue_full: bool
        :param max_request_size:
            The maximum size of a request in bytes. This is also effectively a
            cap on the maximum record size. Note that the server has its own
            cap on record size which may be different from this. This setting
            will limit the number of record batches the producer will send in a
            single request to avoid sending huge requests.
        :type max_request_size: int
        :param sync: Whether calls to `produce` should wait for the message to
            send before returning.  If `True`, an exception will be raised from
            `produce()` if delivery to kafka failed.
        :type sync: bool
        :param delivery_reports: If set to `True`, the producer will maintain a
            thread-local queue on which delivery reports are posted for each
            message produced.  These must regularly be retrieved through
            `get_delivery_report()`, which returns a 2-tuple of
            :class:`pykafka.protocol.Message` and either `None` (for success)
            or an `Exception` in case of failed delivery to kafka. If
            `get_delivery_report()` is not called regularly with this setting enabled,
            memory usage will grow unbounded. This setting is ignored when `sync=True`.
        :type delivery_reports: bool
        :param pending_timeout_ms: The amount of time (in milliseconds) to wait for
            delivery reports to be returned from the broker during a `produce()` call.
            Also, the time in ms to wait during a `stop()` call for all messages to be
            marked as delivered. -1 indicates that these calls should block indefinitely.
            Differs from `ack_timeout_ms` in that `ack_timeout_ms` is a value sent to the
            broker to control the broker-side timeout, while `pending_timeout_ms` is used
            internally by pykafka and not sent to the broker.
        :type pending_timeout_ms:
        :param auto_start: Whether the producer should begin communicating
            with kafka after __init__ is complete. If false, communication
            can be started with `start()`.
        :type auto_start: bool
        :param serializer: A function defining how to serialize messages to be sent
            to Kafka. A function with the signature d(value, partition_key) that
            returns a tuple of (serialized_value, serialized_partition_key). The
            arguments passed to this function are a message's value and partition key,
            and the returned data should be these fields transformed according to the
            client code's serialization logic.  See `pykafka.utils.__init__` for stock
            implemtations.
        :type serializer: function
        """
        self._cluster = cluster
        self._protocol_version = msg_protocol_version(cluster._broker_version)
        self._topic = topic
        self._partitioner = partitioner or RandomPartitioner()
        self._compression = compression
        if self._compression == CompressionType.SNAPPY:
            if platform.python_implementation == 'PyPy':
                log.warning('Caution: python-snappy segfaults when attempting to compress large messages under PyPy')
        self._max_retries = valid_int(max_retries, allow_zero=True)
        self._retry_backoff_ms = valid_int(retry_backoff_ms)
        self._required_acks = valid_int(required_acks, allow_zero=True, allow_negative=True)
        self._ack_timeout_ms = valid_int(ack_timeout_ms, allow_zero=True)
        self._max_queued_messages = valid_int(max_queued_messages, allow_zero=True)
        self._min_queued_messages = max(1, valid_int(min_queued_messages) if not sync else 1)
        self._linger_ms = valid_int(linger_ms, allow_zero=True)
        self._queue_empty_timeout_ms = valid_int(queue_empty_timeout_ms, allow_zero=True,
          allow_negative=True)
        self._block_on_queue_full = block_on_queue_full
        self._max_request_size = valid_int(max_request_size)
        self._synchronous = sync
        self._worker_exception = None
        self._owned_brokers = None
        self._delivery_reports = _DeliveryReportQueue(self._cluster.handler) if delivery_reports or self._synchronous else _DeliveryReportNone()
        self._pending_timeout_ms = pending_timeout_ms
        self._auto_start = auto_start
        self._serializer = serializer
        self._running = False
        self._update_lock = self._cluster.handler.Lock()
        if self._auto_start:
            self.start()

    def __del__(self):
        if log:
            log.debug('Finalising {}'.format(self))
        self.stop()

    def _raise_worker_exceptions(self):
        """Raises exceptions encountered on worker threads"""
        if self._worker_exception is not None:
            reraise(*self._worker_exception)

    def __repr__(self):
        return '<{module}.{name} at {id_}>'.format(module=(self.__class__.__module__),
          name=(self.__class__.__name__),
          id_=(hex(id(self))))

    def __enter__(self):
        """Context manager entry point - start the producer"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit point - stop the producer"""
        self.stop()

    def start(self):
        """Set up data structures and start worker threads"""
        if not self._running:
            self._setup_owned_brokers()
            self._running = True
        self._raise_worker_exceptions()

    def _update(self):
        """Update the producer and cluster after an ERROR_CODE

        Also re-produces messages that were in queues at the time the update
        was triggered
        """
        with self._update_lock:
            if self._owned_brokers is not None:
                for owned_broker in list(self._owned_brokers.values()):
                    owned_broker.stop()

            self._cluster.update()
            queued_messages = self._setup_owned_brokers()
            if len(queued_messages):
                log.debug('Re-producing %d queued messages after update', len(queued_messages))
                for message in queued_messages:
                    self._produce(message)

    def _setup_owned_brokers(self):
        """Instantiate one OwnedBroker per broker

        If there are already OwnedBrokers instantiated, safely stop and flush them
        before creating new ones.
        """
        queued_messages = []
        if self._owned_brokers is not None:
            brokers = list(self._owned_brokers.keys())
            for broker in brokers:
                owned_broker = self._owned_brokers.pop(broker)
                owned_broker.stop()
                while True:
                    batch = owned_broker.flush((self._linger_ms), (self._max_request_size),
                      release_pending=False,
                      wait=False)
                    if not batch:
                        break
                    queued_messages.extend(batch)

        self._owned_brokers = {}
        for partition in self._topic.partitions.values():
            if partition.leader.id not in self._owned_brokers:
                self._owned_brokers[partition.leader.id] = OwnedBroker(self, partition.leader)

        return queued_messages

    def stop(self):
        """Mark the producer as stopped, and wait until all messages to be sent"""

        def get_queue_readers():
            if not self._owned_brokers:
                return []
            else:
                return [owned_broker._queue_reader_worker for owned_broker in self._owned_brokers.values() if owned_broker.running]

        def stop_owned_brokers():
            self._wait_all()
            if self._owned_brokers is not None:
                for owned_broker in self._owned_brokers.values():
                    owned_broker.stop()

        while self._running:
            queue_readers = get_queue_readers()
            stop_owned_brokers()
            if len(queue_readers) == 0:
                self._running = False
            else:
                for queue_reader in queue_readers:
                    queue_reader.join()

    def _produce_has_timed_out(self, start_time):
        """Indicates whether enough time has passed since start_time for a `produce()`
            call to timeout
        """
        if self._pending_timeout_ms == -1:
            return False
        else:
            return time.time() * 1000 - start_time > self._pending_timeout_ms

    def produce(self, message, partition_key=None, timestamp=None):
        """Produce a message.

        :param message: The message to produce (use None to send null)
        :type message: bytes
        :param partition_key: The key to use when deciding which partition to send this
            message to. This key is passed to the `partitioner`, which may or may not
            use it in deciding the partition. The default `RandomPartitioner` does not
            use this key, but the optional `HashingPartitioner` does.
        :type partition_key: bytes
        :param timestamp: The timestamp at which the message is produced (requires
            broker_version >= 0.10.0)
        :type timestamp: `datetime.datetime`
        :return: The :class:`pykafka.protocol.Message` instance that was
            added to the internal message queue
        """
        if self._serializer is None:
            if partition_key is not None:
                if type(partition_key) is not bytes:
                    raise TypeError("Producer.produce accepts a bytes object as partition_key, but it got '%s'", type(partition_key))
                if message is not None:
                    if type(message) is not bytes:
                        raise TypeError("Producer.produce accepts a bytes object as message, but it got '%s'", type(message))
            else:
                if timestamp is not None:
                    if self._protocol_version < 1:
                        raise RuntimeError('Producer.produce got a timestamp with protocol 0')
                raise self._running or ProducerStoppedException()
            if self._serializer is not None:
                message, partition_key = self._serializer(message, partition_key)
        else:
            partitions = list(self._topic.partitions.values())
            partition_id = self._partitioner(partitions, partition_key).id
            msg = Message(value=message, partition_key=partition_key,
              partition_id=partition_id,
              timestamp=timestamp,
              protocol_version=(self._protocol_version),
              delivery_report_q=(self._delivery_reports.queue))
            self._produce(msg)
            if self._synchronous:
                req_time = time.time() * 1000
                reported_msg = None
                while not self._produce_has_timed_out(req_time):
                    self._raise_worker_exceptions()
                    self._cluster.handler.sleep()
                    try:
                        reported_msg, exc = self.get_delivery_report(timeout=1)
                        break
                    except Empty:
                        continue
                    except ValueError:
                        raise ProduceFailureError('Error retrieving delivery report')

                if reported_msg is not msg:
                    raise ProduceFailureError('Delivery report not received after timeout')
                if exc is not None:
                    raise exc
        self._raise_worker_exceptions()
        return msg

    def get_delivery_report(self, block=True, timeout=None):
        """Fetch delivery reports for messages produced on the current thread

        Returns 2-tuples of a `pykafka.protocol.Message` and either `None`
        (for successful deliveries) or `Exception` (for failed deliveries).
        This interface is only available if you enabled `delivery_reports` on
        init (and you did not use `sync=True`)

        :param block: Whether to block on dequeueing a delivery report
        :type block: bool
        :param timeout: How long (in seconds) to block before returning None
        ;type timeout: int
        """
        try:
            return self._delivery_reports.queue.get(block, timeout)
        except AttributeError:
            raise KafkaException('Delivery-reporting is disabled')

    def _produce(self, message):
        """Enqueue a message for the relevant broker
        Attempts to update metadata in response to missing brokers.
        :param message: Message with valid `partition_id`, ready to be sent
        :type message: `pykafka.protocol.Message`
        """
        success = False
        retry = 0
        while not success:
            leader_id = self._topic.partitions[message.partition_id].leader.id
            if leader_id in self._owned_brokers:
                self._owned_brokers[leader_id].enqueue(message)
                success = True
            else:
                retry += 1
                if retry < 10:
                    log.debug('Failed to enqueue produced message. Updating metdata.')
                    self._update()
                else:
                    raise ProduceFailureError('Message could not be enqueued due to missing broker metadata for broker {}'.format(leader_id))
                success = False

    def _mark_as_delivered(self, owned_broker, message_batch, req):
        owned_broker.increment_messages_pending(-1 * len(message_batch))
        req.delivered += len(message_batch)
        for msg in message_batch:
            self._delivery_reports.put(msg)

    def _send_request--- This code section failed: ---

 L. 472         0  LOAD_GLOBAL              ProduceRequest

 L. 473         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _compression

 L. 474         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _required_acks

 L. 475        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _ack_timeout_ms

 L. 476        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _cluster
               18  LOAD_ATTR                _broker_version
               20  LOAD_CONST               ('compression_type', 'required_acks', 'timeout', 'broker_version')
               22  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               24  STORE_FAST               'req'

 L. 478        26  LOAD_CONST               0
               28  LOAD_FAST                'req'
               30  STORE_ATTR               delivered

 L. 479        32  SETUP_LOOP           66  'to 66'
               34  LOAD_FAST                'message_batch'
               36  GET_ITER         
               38  FOR_ITER             64  'to 64'
               40  STORE_FAST               'msg'

 L. 480        42  LOAD_FAST                'req'
               44  LOAD_ATTR                add_message
               46  LOAD_FAST                'msg'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _topic
               52  LOAD_ATTR                name
               54  LOAD_FAST                'msg'
               56  LOAD_ATTR                partition_id
               58  CALL_FUNCTION_3       3  ''
               60  POP_TOP          
               62  JUMP_BACK            38  'to 38'
               64  POP_BLOCK        
             66_0  COME_FROM_LOOP       32  '32'

 L. 481        66  LOAD_GLOBAL              log
               68  LOAD_ATTR                debug
               70  LOAD_STR                 'Sending %d messages to broker %d'

 L. 482        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'message_batch'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_FAST                'owned_broker'
               80  LOAD_ATTR                broker
               82  LOAD_ATTR                id
               84  CALL_FUNCTION_3       3  ''
               86  POP_TOP          

 L. 484        88  LOAD_CODE                <code_object _get_partition_msgs>
               90  LOAD_STR                 'Producer._send_request.<locals>._get_partition_msgs'
               92  MAKE_FUNCTION_0          ''
               94  STORE_FAST               '_get_partition_msgs'

 L. 493        96  SETUP_EXCEPT        376  'to 376'

 L. 494       100  LOAD_FAST                'owned_broker'
              102  LOAD_ATTR                broker
              104  LOAD_ATTR                produce_messages
              106  LOAD_FAST                'req'
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'response'

 L. 495       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _required_acks
              116  LOAD_CONST               0
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   140  'to 140'

 L. 496       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _mark_as_delivered
              126  LOAD_FAST                'owned_broker'
              128  LOAD_FAST                'message_batch'
              130  LOAD_FAST                'req'
              132  CALL_FUNCTION_3       3  ''
              134  POP_TOP          

 L. 497       136  LOAD_CONST               None
              138  RETURN_END_IF    
            140_0  COME_FROM           120  '120'

 L. 501       140  BUILD_LIST_0          0 
              142  STORE_FAST               'to_retry'

 L. 503       144  SETUP_LOOP          372  'to 372'
              146  LOAD_GLOBAL              iteritems
              148  LOAD_FAST                'response'
              150  LOAD_ATTR                topics
              152  CALL_FUNCTION_1       1  ''
              154  GET_ITER         
              156  FOR_ITER            370  'to 370'
              158  UNPACK_SEQUENCE_2     2 
              160  STORE_FAST               'topic'
              162  STORE_FAST               'partitions'

 L. 504       164  SETUP_LOOP          368  'to 368'
              166  LOAD_GLOBAL              iteritems
              168  LOAD_FAST                'partitions'
              170  CALL_FUNCTION_1       1  ''
              172  GET_ITER         
              174  FOR_ITER            366  'to 366'
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'partition'
              180  STORE_FAST               'presponse'

 L. 505       182  LOAD_FAST                'presponse'
              184  LOAD_ATTR                err
              186  LOAD_CONST               0
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   260  'to 260'

 L. 506       194  LOAD_FAST                'req'
              196  LOAD_ATTR                msets
              198  LOAD_FAST                'topic'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'partition'
              204  BINARY_SUBSCR    
              206  LOAD_ATTR                messages
              208  STORE_FAST               'messages'

 L. 507       210  SETUP_LOOP          244  'to 244'
              212  LOAD_GLOBAL              enumerate
              214  LOAD_FAST                'messages'
              216  CALL_FUNCTION_1       1  ''
              218  GET_ITER         
              220  FOR_ITER            242  'to 242'
              222  UNPACK_SEQUENCE_2     2 
              224  STORE_FAST               'i'
              226  STORE_FAST               'message'

 L. 508       228  LOAD_FAST                'presponse'
              230  LOAD_ATTR                offset
              232  LOAD_FAST                'i'
              234  BINARY_ADD       
              236  LOAD_FAST                'message'
              238  STORE_ATTR               offset
              240  JUMP_BACK           220  'to 220'
              242  POP_BLOCK        
            244_0  COME_FROM_LOOP      210  '210'

 L. 509       244  LOAD_FAST                'self'
              246  LOAD_ATTR                _mark_as_delivered
              248  LOAD_FAST                'owned_broker'
              250  LOAD_FAST                'messages'
              252  LOAD_FAST                'req'
              254  CALL_FUNCTION_3       3  ''
              256  POP_TOP          

 L. 510       258  CONTINUE            174  'to 174'

 L. 511       260  LOAD_FAST                'presponse'
              262  LOAD_ATTR                err
              264  LOAD_GLOBAL              NotLeaderForPartition
              266  LOAD_ATTR                ERROR_CODE
              268  COMPARE_OP               ==
              270  POP_JUMP_IF_FALSE   282  'to 282'

 L. 513       274  LOAD_FAST                'self'
              276  LOAD_ATTR                _update
              278  CALL_FUNCTION_0       0  ''
              280  POP_TOP          
            282_0  COME_FROM           270  '270'

 L. 514       282  LOAD_STR                 'Produce request for {}/{} to {}:{} failed with error code {}.'
              284  LOAD_ATTR                format

 L. 515       286  LOAD_FAST                'topic'

 L. 516       288  LOAD_FAST                'partition'

 L. 517       290  LOAD_FAST                'owned_broker'
              292  LOAD_ATTR                broker
              294  LOAD_ATTR                host

 L. 518       296  LOAD_FAST                'owned_broker'
              298  LOAD_ATTR                broker
              300  LOAD_ATTR                port

 L. 519       302  LOAD_FAST                'presponse'
              304  LOAD_ATTR                err
              306  CALL_FUNCTION_5       5  ''
              308  STORE_FAST               'info'

 L. 520       310  LOAD_GLOBAL              log
              312  LOAD_ATTR                warning
              314  LOAD_FAST                'info'
              316  CALL_FUNCTION_1       1  ''
              318  POP_TOP          

 L. 521       320  LOAD_GLOBAL              ERROR_CODES
              322  LOAD_FAST                'presponse'
              324  LOAD_ATTR                err
              326  BINARY_SUBSCR    
              328  LOAD_FAST                'info'
              330  CALL_FUNCTION_1       1  ''
              332  STORE_DEREF              'exc'

 L. 522       334  LOAD_FAST                'to_retry'
              336  LOAD_ATTR                extend

 L. 523       338  LOAD_CLOSURE             'exc'
              340  BUILD_TUPLE_1         1 
              342  LOAD_GENEXPR             '<code_object <genexpr>>'
              344  LOAD_STR                 'Producer._send_request.<locals>.<genexpr>'
              346  MAKE_FUNCTION_8          'closure'

 L. 524       348  LOAD_FAST                '_get_partition_msgs'
              350  LOAD_FAST                'partition'
              352  LOAD_FAST                'req'
              354  CALL_FUNCTION_2       2  ''
              356  GET_ITER         
              358  CALL_FUNCTION_1       1  ''
              360  CALL_FUNCTION_1       1  ''
              362  POP_TOP          
              364  JUMP_BACK           174  'to 174'
              366  POP_BLOCK        
            368_0  COME_FROM_LOOP      164  '164'
              368  JUMP_BACK           156  'to 156'
              370  POP_BLOCK        
            372_0  COME_FROM_LOOP      144  '144'
              372  POP_BLOCK        
              374  JUMP_FORWARD        472  'to 472'
            376_0  COME_FROM_EXCEPT     96  '96'

 L. 525       376  DUP_TOP          
              378  LOAD_GLOBAL              SocketDisconnectedError
              380  LOAD_GLOBAL              struct
              382  LOAD_ATTR                error
              384  BUILD_TUPLE_2         2 
              386  COMPARE_OP               exception-match
              388  POP_JUMP_IF_FALSE   470  'to 470'
              392  POP_TOP          
              394  STORE_DEREF              'exc'
              396  POP_TOP          
              398  SETUP_FINALLY       460  'to 460'

 L. 526       400  LOAD_GLOBAL              log
              402  LOAD_ATTR                warning
              404  LOAD_STR                 'Error encountered when producing to broker %s:%s. Retrying.'

 L. 527       406  LOAD_FAST                'owned_broker'
              408  LOAD_ATTR                broker
              410  LOAD_ATTR                host

 L. 528       412  LOAD_FAST                'owned_broker'
              414  LOAD_ATTR                broker
              416  LOAD_ATTR                port
              418  CALL_FUNCTION_3       3  ''
              420  POP_TOP          

 L. 529       422  LOAD_FAST                'self'
              424  LOAD_ATTR                _update
              426  CALL_FUNCTION_0       0  ''
              428  POP_TOP          

 L. 531       430  LOAD_CLOSURE             'exc'
              432  BUILD_TUPLE_1         1 
              434  LOAD_LISTCOMP            '<code_object <listcomp>>'
              436  LOAD_STR                 'Producer._send_request.<locals>.<listcomp>'
              438  MAKE_FUNCTION_8          'closure'

 L. 532       440  LOAD_GLOBAL              iteritems
              442  LOAD_FAST                'req'
              444  LOAD_ATTR                msets
              446  CALL_FUNCTION_1       1  ''
              448  GET_ITER         
              450  CALL_FUNCTION_1       1  ''
              452  STORE_FAST               'to_retry'
              454  POP_BLOCK        
              456  POP_EXCEPT       
              458  LOAD_CONST               None
            460_0  COME_FROM_FINALLY   398  '398'
              460  LOAD_CONST               None
              462  STORE_DEREF              'exc'
              464  DELETE_DEREF             'exc'
              466  END_FINALLY      
              468  JUMP_FORWARD        472  'to 472'
              470  END_FINALLY      
            472_0  COME_FROM           468  '468'
            472_1  COME_FROM           374  '374'

 L. 536       472  LOAD_GLOBAL              log
              474  LOAD_ATTR                debug
              476  LOAD_STR                 'Successfully sent {}/{} messages to broker {}'
              478  LOAD_ATTR                format

 L. 537       480  LOAD_FAST                'req'
              482  LOAD_ATTR                delivered
              484  LOAD_GLOBAL              len
              486  LOAD_FAST                'message_batch'
              488  CALL_FUNCTION_1       1  ''
              490  LOAD_FAST                'owned_broker'
              492  LOAD_ATTR                broker
              494  LOAD_ATTR                id
              496  CALL_FUNCTION_3       3  ''
              498  CALL_FUNCTION_1       1  ''
              500  POP_TOP          

 L. 539       502  LOAD_FAST                'to_retry'
              504  POP_JUMP_IF_FALSE   674  'to 674'

 L. 540       508  LOAD_FAST                'self'
              510  LOAD_ATTR                _cluster
              512  LOAD_ATTR                handler
              514  LOAD_ATTR                sleep
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                _retry_backoff_ms
              520  LOAD_CONST               1000
              522  BINARY_TRUE_DIVIDE
              524  CALL_FUNCTION_1       1  ''
              526  POP_TOP          

 L. 541       528  LOAD_FAST                'owned_broker'
              530  LOAD_ATTR                increment_messages_pending
              532  LOAD_CONST               -1
              534  LOAD_GLOBAL              len
              536  LOAD_FAST                'to_retry'
              538  CALL_FUNCTION_1       1  ''
              540  BINARY_MULTIPLY  
              542  CALL_FUNCTION_1       1  ''
              544  POP_TOP          

 L. 542       546  SETUP_LOOP          674  'to 674'
              548  LOAD_FAST                'to_retry'
              550  GET_ITER         
              552  FOR_ITER            672  'to 672'
              554  UNPACK_SEQUENCE_2     2 
              556  STORE_FAST               'mset'
              558  STORE_DEREF              'exc'

 L. 546       560  LOAD_GLOBAL              type
              562  LOAD_DEREF               'exc'
              564  CALL_FUNCTION_1       1  ''
              566  LOAD_GLOBAL              InvalidMessageSize

 L. 547       568  LOAD_GLOBAL              MessageSizeTooLarge
              570  BUILD_TUPLE_2         2 
              572  COMPARE_OP               in
              574  STORE_FAST               'non_recoverable'

 L. 548       576  SETUP_LOOP          668  'to 668'
              578  LOAD_FAST                'mset'
              580  LOAD_ATTR                messages
              582  GET_ITER         
              584  FOR_ITER            666  'to 666'
              586  STORE_FAST               'msg'

 L. 549       588  LOAD_FAST                'non_recoverable'
              590  POP_JUMP_IF_TRUE    608  'to 608'
              594  LOAD_FAST                'msg'
              596  LOAD_ATTR                produce_attempt
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                _max_retries
              602  COMPARE_OP               >=
            604_0  COME_FROM           590  '590'
              604  POP_JUMP_IF_FALSE   638  'to 638'

 L. 550       608  LOAD_FAST                'self'
              610  LOAD_ATTR                _delivery_reports
              612  LOAD_ATTR                put
              614  LOAD_FAST                'msg'
              616  LOAD_DEREF               'exc'
              618  CALL_FUNCTION_2       2  ''
              620  POP_TOP          

 L. 551       622  LOAD_GLOBAL              log
              624  LOAD_ATTR                error
              626  LOAD_STR                 'Message not delivered!! %r'
              628  LOAD_DEREF               'exc'
              630  BINARY_MODULO    
              632  CALL_FUNCTION_1       1  ''
              634  POP_TOP          
              636  JUMP_FORWARD        662  'to 662'
              638  ELSE                     '662'

 L. 553       638  LOAD_FAST                'msg'
              640  DUP_TOP          
              642  LOAD_ATTR                produce_attempt
              644  LOAD_CONST               1
              646  INPLACE_ADD      
              648  ROT_TWO          
              650  STORE_ATTR               produce_attempt

 L. 554       652  LOAD_FAST                'self'
              654  LOAD_ATTR                _produce
              656  LOAD_FAST                'msg'
              658  CALL_FUNCTION_1       1  ''
              660  POP_TOP          
            662_0  COME_FROM           636  '636'
              662  JUMP_BACK           584  'to 584'
              666  POP_BLOCK        
            668_0  COME_FROM_LOOP      576  '576'
              668  JUMP_BACK           552  'to 552'
              672  POP_BLOCK        
            674_0  COME_FROM_LOOP      546  '546'
            674_1  COME_FROM           504  '504'

Parse error at or near `DELETE_DEREF' instruction at offset 464

    def _wait_all(self):
        """Block until all pending messages are sent or until pending_timeout_ms

        "Pending" messages are those that have been used in calls to `produce`
        and have not yet been acknowledged in a response from the broker
        """
        log.info('Blocking until all messages are sent or until pending_timeout_ms')
        start_time = time.time() * 1000
        while any(q.message_is_pending() for q in itervalues(self._owned_brokers)) and not self._produce_has_timed_out(start_time):
            self._cluster.handler.sleep(0.3)
            self._raise_worker_exceptions()


class OwnedBroker(object):
    """OwnedBroker"""

    def __init__(self, producer, broker, auto_start=True):
        self.producer = weakref.proxy(producer)
        self.broker = broker
        self.lock = self.producer._cluster.handler.RLock()
        self.flush_ready = self.producer._cluster.handler.Event()
        self.has_message = self.producer._cluster.handler.Event()
        self.slot_available = self.producer._cluster.handler.Event()
        self.queue = deque()
        self.messages_pending = 0
        self.running = True
        self._auto_start = auto_start
        if self._auto_start:
            self.start()

    def cleanup(self):
        if not self.slot_available.is_set():
            self.slot_available.set()

    def start(self):

        def queue_reader():
            while self.running:
                try:
                    batch = self.flush(self.producer._linger_ms, self.producer._max_request_size)
                    if batch:
                        self.producer._send_request(batch, self)
                except Exception:
                    self.producer._worker_exception = sys.exc_info()
                    break

            self.cleanup()
            log.info('Worker exited for broker %s:%s', self.broker.host, self.broker.port)

        log.info('Starting new produce worker for broker %s', self.broker.id)
        name = 'pykafka.OwnedBroker.queue_reader for broker {}'.format(self.broker.id)
        self._queue_reader_worker = self.producer._cluster.handler.spawn(queue_reader,
          name=name)

    def stop(self):
        with self.lock:
            if not self.has_message.is_set():
                self.has_message.set()
        self.running = False

    def increment_messages_pending(self, amnt):
        with self.lock:
            self.messages_pending += amnt
            self.messages_pending = max(0, self.messages_pending)

    def message_is_pending(self):
        """
        Indicates whether there are currently any messages that have been
            `produce()`d and not yet sent to the broker
        """
        return self.messages_pending > 0

    def enqueue(self, message):
        """Push message onto the queue

        :param message: The message to push onto the queue
        :type message: `pykafka.protocol.Message`
        """
        self._wait_for_slot_available()
        with self.lock:
            self.queue.appendleft(message)
            self.increment_messages_pending(1)
            if len(self.queue) >= self.producer._min_queued_messages:
                if not self.flush_ready.is_set():
                    self.flush_ready.set()
            if not self.has_message.is_set():
                self.has_message.set()

    def flush(self, linger_ms, max_request_size, release_pending=False, wait=True):
        """Pop messages from the end of the queue

        :param linger_ms: How long (in milliseconds) to wait for the queue
            to contain messages before flushing
        :type linger_ms: int
        :param max_request_size: The max size should each batch of messages
            should be in bytes
        :type max_request_size: int
        :param release_pending: Whether to decrement the messages_pending
            counter when the queue is flushed. True means that the messages
            popped from the queue will be discarded unless re-enqueued
            by the caller.
        :type release_pending: bool
        :param wait: If True, wait for the event indicating a flush is ready. If False,
            attempt a flush immediately without waiting
        :type wait: bool
        """
        self._wait_for_has_message(self.producer._queue_empty_timeout_ms)
        if wait:
            self._wait_for_flush_ready(linger_ms)
        with self.lock:
            batch = []
            batch_size_in_bytes = 0
            while len(self.queue) > 0:
                if not self.running:
                    return []
                peeked_message = self.queue[(-1)]
                if peeked_message:
                    if peeked_message.value is not None:
                        if len(peeked_message) > max_request_size:
                            exc = MessageSizeTooLarge('Message size larger than max_request_size: {}'.format(max_request_size))
                            log.warning(exc)
                            message = self.queue.pop()
                            if peeked_message.delivery_report_q is not None:
                                peeked_message.delivery_report_q.put((message, exc))
                            self.increment_messages_pending(-1)
                            continue
                        elif batch_size_in_bytes + len(peeked_message) > max_request_size:
                            log.debug('max_request_size reached. producing batch')
                            self.flush_ready.set()
                            break
                message = self.queue.pop()
                batch_size_in_bytes += len(message)
                batch.append(message)

            if release_pending:
                self.increment_messages_pending(-1 * len(batch))
            if not self.slot_available.is_set():
                self.slot_available.set()
        if not self.running:
            return []
        else:
            return batch

    def _wait_for_flush_ready(self, linger_ms):
        """Block until the queue is ready to be flushed

        If the queue does not contain at least one message after blocking for
        `linger_ms` milliseconds, return.

        :param linger_ms: How long (in milliseconds) to wait for the queue
            to contain messages before returning
        :type linger_ms: int
        """
        if len(self.queue) < self.producer._min_queued_messages:
            with self.lock:
                if len(self.queue) < self.producer._min_queued_messages:
                    self.flush_ready.clear()
            if linger_ms > 0:
                self.flush_ready.wait(linger_ms / 1000)

    def _wait_for_has_message(self, timeout_ms):
        """Block until the queue has at least one slot containing a message

        :param timeout_ms: The amount of time in milliseconds to wait for a message
            to be enqueued. -1 indicates infinite waiting; in this case a thread waiting
            on this call can only be killed by a call to `stop()`.
        :type timeout_ms: int
        """
        if len(self.queue) == 0:
            if self.running:
                with self.lock:
                    if len(self.queue) == 0:
                        if self.running:
                            self.has_message.clear()
                if timeout_ms != -1:
                    self.has_message.wait(timeout_ms / 1000)
                else:
                    while not self.has_message.is_set():
                        self.producer._cluster.handler.sleep()
                        self.has_message.wait(5)

    def _wait_for_slot_available(self):
        """Block until the queue has at least one slot not containing a message"""
        if len(self.queue) >= self.producer._max_queued_messages:
            with self.lock:
                if len(self.queue) >= self.producer._max_queued_messages:
                    self.slot_available.clear()
            if self.producer._block_on_queue_full:
                while not self.slot_available.is_set():
                    self.producer._cluster.handler.sleep()
                    self.slot_available.wait(5)

            else:
                raise ProducerQueueFullError('Queue full for broker %d', self.broker.id)


class _DeliveryReportQueue(threading.local):
    """_DeliveryReportQueue"""

    def __init__(self, handler):
        self.queue = handler.Queue()

    @staticmethod
    def put(msg, exc=None):
        msg.delivery_report_q.put((msg, exc))


class _DeliveryReportNone(object):
    """_DeliveryReportNone"""

    def __init__(self):
        self.queue = None

    @staticmethod
    def put(msg, exc=None):
        pass