# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/link.py
# Compiled at: 2019-08-07 08:55:31
# Size of source mod 2**32: 47620 bytes
import math
from threading import Lock, current_thread
from multiprocessing import Pipe
from pickle5 import pickle
import time, argparse
from uuid import uuid4
from os import environ
from confluent_kafka import Producer, Consumer, KafkaError
import signal
from . import utils
from .electron import Electron
from .callback import Callback
from .logger import Logger
from .custom_queue import ThreadingQueue
from .custom_threading import Thread, ThreadPool
from .custom_multiprocessing import Process
from connectors.aerospike import AerospikeConnector
from connectors.mongodb import MongodbConnector
from .structures import CircularOrderedSet

class Link:

    def __init__(self, log_level='INFO', input_mode='parity', exp_window_size=900, synchronous=False, sequential=False, uid_consumer_group=False, num_rpc_threads=1, num_main_threads=1, input_topics=None, output_topics=None, kafka_endpoint='localhost:9092', consumer_group=None, consumer_timeout=300, aerospike_endpoint=None, mongodb_endpoint=None):
        if 'CATENAE_DOCKER' in environ and bool(environ['CATENAE_DOCKER']):
            self._uid = environ['HOSTNAME']
        else:
            self._uid = utils.keccak256(str(uuid4()))[:12]
        self._set_log_level(log_level)
        self.logger = Logger(self, self._log_level)
        self.logger.log(f"log level: {self._log_level}")
        self._started = False
        self._stopped = False
        self._input_topics_lock = Lock()
        self._rpc_lock = Lock()
        self._start_stop_lock = Lock()
        self.rpc_instance_topic = f"catenae_rpc_{self._uid}"
        self.rpc_group_topic = f"catenae_rpc_{self.__class__.__name__.lower()}"
        self.rpc_broadcast_topic = 'catenae_rpc_broadcast'
        self._rpc_topics = [self.rpc_instance_topic, self.rpc_group_topic, self.rpc_broadcast_topic]
        self._known_message_ids = CircularOrderedSet(50)
        self._load_args()
        self._set_execution_opts(input_mode, exp_window_size, synchronous, sequential, num_rpc_threads, num_main_threads, input_topics, output_topics, kafka_endpoint, consumer_timeout)
        self._set_connectors_properties(aerospike_endpoint, mongodb_endpoint)
        self._set_consumer_group(consumer_group, uid_consumer_group)
        self._input_messages = ThreadingQueue()
        self._output_messages = ThreadingQueue()
        self._changed_input_topics = False

    TIMEOUT = 0.5
    COMMIT_ATTEMPTS = 30

    @property
    def input_topics(self):
        return self._input_topics

    @property
    def output_topics(self):
        return self._output_topics

    @property
    def consumer_group(self):
        return self._consumer_group

    @property
    def args(self):
        return self._args

    @property
    def uid(self):
        return self._uid

    @property
    def aerospike(self):
        return self._aerospike

    @property
    def mongodb(self):
        return self._mongodb

    def start(self, embedded=False):
        with self._start_stop_lock:
            if self._started:
                return
            self._started = True
        if self._kafka_endpoint:
            self._set_kafka_common_properties()
            self._setup_kafka_producers()
        self._set_connectors()
        try:
            try:
                self.setup()
                self.logger.log(f"link {self._uid} is starting...")
                self._launch_tasks()
            except Exception:
                try:
                    self.suicide('Exception during the execution of setup()', exception=True)
                except SystemExit:
                    pass

        finally:
            self.logger.log(f"link {self._uid} is running")
            if embedded:
                Thread(target=(self._join_tasks)).start()
            else:
                self._setup_signals_handler()
                self._join_tasks()

    def _join_tasks(self):
        if hasattr(self, '_generator_main_thread'):
            self._generator_main_thread.join()
        if self._kafka_endpoint:
            if hasattr(self, '_producer_thread'):
                self._producer_thread.join()
            if hasattr(self, '_input_handler_thread'):
                self._input_handler_thread.join()
            if hasattr(self, '_consumer_rpc_thread'):
                self._consumer_rpc_thread.join()
            if hasattr(self, '_consumer_main_thread'):
                self._consumer_main_thread.join()
            if hasattr(self, '_transform_rpc_executor'):
                for i, thread in enumerate(self._transform_rpc_executor.threads):
                    self._join_if_not_current_thread(thread)

            if hasattr(self, '_transform_main_executor'):
                for i, thread in enumerate(self._transform_main_executor.threads):
                    self._join_if_not_current_thread(thread)

        self.logger.log(f"link {self.uid} stopped")

    def setup(self):
        pass

    def transform(self, _):
        for thread in self._transform_main_executor.threads:
            thread.stop()

    def finish(self):
        pass

    def generator(self):
        self.logger.log('Generator method undefined. Disabled.', level='debug')
        raise SystemExit

    def send(self, output_content, topic=None, callback=None, callback_args=None, callback_kwargs=None, synchronous=None):
        if isinstance(output_content, Electron):
            if topic:
                output_content.topic = topic
            electron = output_content.copy()
        elif not isinstance(output_content, list):
            electron = Electron(value=output_content, topic=topic, unpack_if_string=True)
        else:
            for i, item in enumerate(output_content):
                if i == len(output_content) - 1:
                    self.send(item, topic=topic, callback=callback, synchronous=synchronous)
                else:
                    self.send(item, topic=topic, synchronous=synchronous)

            return
        if callback is not None:
            electron.callbacks.append(Callback(callback, callback_args, callback_kwargs))
        else:
            if synchronous is None:
                synchronous = self._synchronous
            if synchronous:
                self._produce(electron, synchronous=synchronous)
            else:
                self._output_messages.put(electron)

    def add_input_topic(self, input_topic):
        with self._input_topics_lock:
            if input_topic not in self._input_topics:
                self._input_topics.append(input_topic)
                if self._input_mode == 'exp':
                    self._set_input_topic_assignments()
                self._changed_input_topics = True
                self.logger.log(f"added input {input_topic}")

    def remove_input_topic(self, input_topic):
        with self._input_topics_lock:
            if input_topic in self._input_topics:
                self._input_topics.remove(input_topic)
                if self._input_mode == 'exp':
                    self._set_input_topic_assignments()
                self._changed_input_topics = True
                self.logger.log(f"removed input {input_topic}")

    def suicide(self, message=None, exception=False):
        with self._start_stop_lock:
            if self._stopped:
                return
            self._stopped = True
        self.finish()
        if message is None:
            message = '[SUICIDE]'
        else:
            message = f"[SUICIDE] {message}"
        if exception:
            self.logger.log(message, level='exception')
        else:
            self.logger.log(message, level='warn')
        while not self._started:
            time.sleep(Link.TIMEOUT)

        if hasattr(self, '_generator_main_thread'):
            self._generator_main_thread.stop()
        self.logger.log('stopping threads...')
        if self._kafka_endpoint:
            if hasattr(self, '_producer_thread'):
                self._producer_thread.stop()
            if hasattr(self, '_input_handler_thread'):
                self._input_handler_thread.stop()
            if hasattr(self, '_consumer_rpc_thread'):
                self._consumer_rpc_thread.stop()
            if hasattr(self, '_consumer_main_thread'):
                self._consumer_main_thread.stop()
            if hasattr(self, '_transform_rpc_executor'):
                for thread in self._transform_rpc_executor.threads:
                    thread.stop()

            if hasattr(self, '_transform_main_executor'):
                for thread in self._transform_main_executor.threads:
                    thread.stop()

        raise SystemExit

    def loop(self, target, args=None, kwargs=None, interval=0, wait=False):
        loop_task_kwargs = {'target':target, 
         'args':args,  'kwargs':kwargs,  'interval':interval,  'wait':wait}
        loop_thread = Thread(target=(self._loop_task), kwargs=loop_task_kwargs)
        loop_thread.start()
        return loop_thread

    def launch_thread(self, target, args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        thread = Thread(target=target, args=args, kwargs=kwargs)
        thread.start()
        return thread

    def launch_process(self, target, args=None, kwargs=None):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        process = Process(target=target, args=args, kwargs=kwargs)
        process.start()
        return process

    def _set_execution_opts(self, input_mode, exp_window_size, synchronous, sequential, num_rpc_threads, num_main_threads, input_topics, output_topics, kafka_endpoint, consumer_timeout):
        if not hasattr(self, '_input_mode'):
            self._input_mode = input_mode
        else:
            self.logger.log(f"input_mode: {self._input_mode}")
            self._exp_window_size = hasattr(self, '_exp_window_size') or exp_window_size
            if self._input_mode == 'exp':
                self.logger.log(f"exp_window_size: {self._exp_window_size}")
            elif hasattr(self, '_synchronous'):
                synchronous = self._synchronous
            else:
                if hasattr(self, '_sequential'):
                    sequential = self._sequential
                elif synchronous:
                    self._synchronous = True
                    self._sequential = True
                else:
                    self._synchronous = False
                    self._sequential = sequential
                if self._synchronous:
                    self.logger.log('execution mode: sync + seq')
                elif self._sequential:
                    self.logger.log('execution mode: async + seq')
                else:
                    self.logger.log('execution mode: async')
            if hasattr(self, '_num_rpc_threads'):
                num_rpc_threads = self._num_rpc_threads
            if hasattr(self, '_num_main_threads'):
                num_main_threads = self._num_main_threads
            elif synchronous or sequential:
                self._num_main_threads = 1
                self._num_rpc_threads = 1
            else:
                self._num_rpc_threads = num_rpc_threads
                self._num_main_threads = num_main_threads
            self.logger.log(f"num_rpc_threads: {self._num_rpc_threads}")
            self.logger.log(f"num_main_threads: {self._num_main_threads}")
            if not hasattr(self, '_input_topics'):
                self._input_topics = input_topics
            self.logger.log(f"input_topics: {self._input_topics}")
            if not hasattr(self, '_output_topics'):
                self._output_topics = output_topics
            self.logger.log(f"output_topics: {self._output_topics}")
            if not hasattr(self, '_kafka_endpoint'):
                self._kafka_endpoint = kafka_endpoint
            self.logger.log(f"kafka_endpoint: {self._kafka_endpoint}")
            self._consumer_timeout = hasattr(self, '_consumer_timeout') or consumer_timeout
        self.logger.log(f"consumer_timeout: {self._consumer_timeout}")
        self._consumer_timeout = self._consumer_timeout * 1000

    def _set_connectors_properties(self, aerospike_endpoint, mongodb_endpoint):
        self._set_aerospike_properties(aerospike_endpoint)
        if hasattr(self, '_aerospike_host'):
            self.logger.log(f"aerospike_host: {self._aerospike_host}")
        if hasattr(self, '_aerospike_port'):
            self.logger.log(f"aerospike_port: {self._aerospike_port}")
        self._set_mongodb_properties(mongodb_endpoint)
        if hasattr(self, '_mongodb_host'):
            self.logger.log(f"mongodb_host: {self._mongodb_host}")
        if hasattr(self, '_mongodb_port'):
            self.logger.log(f"mongodb_port: {self._mongodb_port}")

    def _loop_task(self, target, args=None, kwargs=None, interval=None, wait=False):
        if wait:
            time.sleep(interval)
        else:
            if args is None:
                args = []
            if kwargs is None:
                kwargs = {}
            args = isinstance(args, list) or [
             args]
        while not current_thread().will_stop:
            try:
                self.logger.log(f"new loop iteration ({target.__name__})", level='debug')
                start_timestamp = utils.get_timestamp()
                target(*args, **kwargs)
                sleep_seconds = interval - utils.get_timestamp() + start_timestamp
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)
            except Exception:
                self.logger.log(f"exception raised when executing the loop: {target.__name__}", level='exception')

    def _signal_handler(self, sig, frame):
        if sig == signal.SIGINT:
            signal_name = 'SIGINT'
        elif sig == signal.SIGTERM:
            signal_name = 'SIGINT'
        elif sig == signal.SIGQUIT:
            signal_name = 'SIGQUIT'
        self.suicide(f"({signal_name})")

    def rpc_call(self, to='broadcast', method=None, args=None, kwargs=None):
        """ 
        Send a Kafka message which will be interpreted as a RPC call by the receiver module.
        """
        if args is None:
            args = []
        else:
            if kwargs is None:
                kwargs = {}
            if not isinstance(args, list):
                args = [
                 args]
            assert method
        topic = f"catenae_rpc_{to.lower()}"
        electron = Electron(value={'method':method, 
         'context':{'group':self._consumer_group, 
          'uid':self._uid}, 
         'args':args, 
         'kwargs':kwargs},
          topic=topic)
        self.send(electron, synchronous=True)

    def _rpc_call(self, electron, commit_callback):
        with self._rpc_lock:
            if 'method' not in electron.value:
                self.logger.log(f"invalid RPC invocation: {electron.value}", level='error')
                return
            try:
                try:
                    context = electron.value['context']
                    self.logger.log(f"RPC invocation from {context['uid']} ({context['group']})", level='debug')
                    args = [
                     context] + electron.value['args']
                    kwargs = electron.value['kwargs']
                    (getattr(self, electron.value['method']))(*args, **kwargs)
                except Exception:
                    self.logger.log(f"error when invoking {method} remotely", level='exception')

            finally:
                commit_callback.execute()

    def _join_if_not_current_thread(self, thread):
        if thread is not current_thread():
            thread.join()

    def _kafka_producer(self):
        while not current_thread().will_stop:
            try:
                electron = self._output_messages.get(timeout=(Link.TIMEOUT), block=False)
            except ThreadingQueue.EmptyError:
                continue

            self._produce(electron)

    def _produce(self, electron, synchronous=None):
        if not isinstance(electron, Electron):
            raise ValueError
        else:
            partition_key = None
            if electron.key:
                if isinstance(electron.key, str):
                    partition_key = electron.key.encode('utf-8')
                else:
                    partition_key = pickle.dumps((electron.key), protocol=(pickle.HIGHEST_PROTOCOL))
            elif self._sequential:
                partition_key = self._uid.encode('utf-8')
            if not electron.topic:
                if not self._output_topics:
                    self.suicide('electron / default output topic unset')
                electron.topic = self._output_topics[0]
            elif electron.unpack_if_string:
                if isinstance(electron.value, str):
                    serialized_electron = electron.value
                else:
                    serialized_electron = pickle.dumps((electron.get_sendable()), protocol=(pickle.HIGHEST_PROTOCOL))
                if synchronous is None:
                    synchronous = self._synchronous
                if synchronous:
                    producer = self._sync_producer
            else:
                producer = self._async_producer
            try:
                producer.produce(topic=(electron.topic), key=partition_key, value=serialized_electron)
                if synchronous:
                    producer.flush()
                else:
                    producer.poll(0)
                self.logger.log('electron produced', level='debug')
                for callback in electron.callbacks:
                    callback.execute()

            except Exception:
                self.suicide('Kafka producer error', exception=True)

    def _transform(self, electron, commit_callback):
        with self._rpc_lock:
            try:
                transform_result = self.transform(electron)
                self.logger.log('electron transformed', level='debug')
            except Exception:
                self.suicide('exception during the execution of "transform"', exception=True)

            transform_callback = Callback()
            if not isinstance(transform_result, tuple):
                electrons = transform_result
            else:
                electrons = transform_result[0]
            if len(transform_result) > 1:
                transform_callback.target = transform_result[1]
                if len(transform_result) > 2:
                    if isinstance(transform_result[2], dict):
                        transform_callback.kwargs = transform_result[2]
                    else:
                        transform_callback.args = transform_result[2]
            elif electrons is None:
                if transform_callback:
                    transform_callback.execute()
                if commit_callback:
                    commit_callback.execute()
                return
                if isinstance(electrons, list):
                    real_electrons = []
                    for electron in electrons:
                        if isinstance(electron, Electron):
                            real_electrons.append(electron)
                        else:
                            real_electrons.append(Electron(value=electron, unpack_if_string=True))

                    electrons = real_electrons
            elif isinstance(electrons, Electron):
                electrons = [
                 electrons]
            else:
                electrons = [
                 Electron(value=electrons)]
            if transform_callback:
                electrons[(-1)].callbacks.append(transform_callback)
            if commit_callback:
                electrons[(-1)].callbacks.append(commit_callback)
            for electron in electrons:
                if self._synchronous:
                    self._produce(electron)
                else:
                    self._output_messages.put(electron)

    def _input_handler(self):
        while not current_thread().will_stop:
            self.logger.log('waiting for a new electron to transform...', level='debug')
            try:
                queue_item = self._input_messages.get(timeout=(Link.TIMEOUT), block=False)
            except ThreadingQueue.EmptyError:
                continue

            commit_callback = Callback(mode=(Callback.COMMIT_KAFKA_MESSAGE))
            if isinstance(queue_item, tuple):
                commit_callback.target = queue_item[1]
                if len(queue_item) > 2:
                    if isinstance(queue_item[2], list):
                        commit_callback.args = queue_item[2]
                    elif isinstance(queue_item[2], dict):
                        commit_callback.kwargs = queue_item[2]
                message = queue_item[0]
            else:
                message = queue_item
            if self._is_message_known(message):
                continue
            self._mark_known_message(message)
            self.logger.log('electron received', level='debug')
            try:
                electron = Electron(value=(message.value().decode('utf-8')))
            except Exception:
                electron = pickle.loads(message.value())

            message_timestamp = message.timestamp()[1]
            electron.timestamp = message_timestamp
            electron.previous_topic = message.topic()
            electron.topic = None
            if electron.previous_topic in self._rpc_topics:
                self._transform_rpc_executor.submit(self._rpc_call, [electron, commit_callback])
            else:
                self._transform_main_executor.submit(self._transform, [electron, commit_callback])

    @staticmethod
    def _get_message_id(message):
        message_id = f"{message.topic()}_{message.partition()}_{message.offset()}"
        return message_id

    def _is_message_known(self, message):
        """ Avoid processing repeated messages. This is not mandatory for RPC 
        calls / synchronous mode"""
        message_id = Link._get_message_id(message)
        if message_id in self._known_message_ids:
            self.logger.log(f"Received known message (topic_partition_offset): {message_id}", level='debug')
            return True
        return False

    def _mark_known_message(self, message):
        message_id = Link._get_message_id(message)
        self._known_message_ids.add(message_id)

    def _break_consumer_loop(self, subscription):
        return len(subscription) > 1 and self._input_mode != 'parity'

    def _commit_kafka_message(self, consumer, message):
        commited = False
        attempts = 0
        self.logger.log(f"trying to commit the message {message.value()}", level='debug')
        while not commited:
            if attempts > 1:
                self.logger.log(f"trying to commit a message (attempt {attempts}/30)", level='warn')
            try:
                consumer.commit(message=message, asynchronous=False)
                commited = True
            except Exception:
                self.logger.log(f"could not commit the message {message.value()}", level='exception')
                attempts += 1
                if attempts == Link.COMMIT_ATTEMPTS:
                    self.suicide()
                else:
                    time.sleep(1)

        self.logger.log(f"message {message.value()} commited", level='debug')

    def _kafka_rpc_consumer(self):
        properties = dict(self._kafka_consumer_synchronous_properties)
        consumer = Consumer(properties)
        self.logger.log(f"[RPC] consumer properties: {utils.dump_dict_pretty(properties)}", level='debug')
        subscription = list(self._rpc_topics)
        consumer.subscribe(subscription)
        self.logger.log(f"[RPC] listening on: {subscription}")
        while not current_thread().will_stop:
            try:
                message = consumer.poll(Link.TIMEOUT)
                if message:
                    if not message.key():
                        if not (message.value() or ):
                            continue
                else:
                    break
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        self.suicide(str(message.error()))
                self._input_messages.put((message, self._commit_kafka_message, [consumer, message]))
            except Exception:
                try:
                    consumer.close()
                finally:
                    self.logger.log('stopped RPC input')
                    self.suicide('Kafka consumer error', exception=True)

        consumer.close()

    def _kafka_main_consumer--- This code section failed: ---

 L. 740         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _synchronous
                4  POP_JUMP_IF_FALSE    18  'to 18'

 L. 741         6  LOAD_GLOBAL              dict
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _kafka_consumer_synchronous_properties
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'properties'
               16  JUMP_FORWARD         28  'to 28'
             18_0  COME_FROM             4  '4'

 L. 743        18  LOAD_GLOBAL              dict
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _kafka_consumer_common_properties
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'properties'
             28_0  COME_FROM            16  '16'

 L. 745        28  LOAD_GLOBAL              Consumer
               30  LOAD_FAST                'properties'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'consumer'

 L. 746        36  LOAD_FAST                'self'
               38  LOAD_ATTR                logger
               40  LOAD_ATTR                log
               42  LOAD_STR                 '[MAIN] consumer properties: '
               44  LOAD_GLOBAL              utils
               46  LOAD_METHOD              dump_dict_pretty
               48  LOAD_FAST                'properties'
               50  CALL_METHOD_1         1  ''
               52  FORMAT_VALUE          0  ''
               54  BUILD_STRING_2        2 
               56  LOAD_STR                 'debug'
               58  LOAD_CONST               ('level',)
               60  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               62  POP_TOP          

 L. 748     64_66  SETUP_LOOP          668  'to 668'
               68  LOAD_GLOBAL              current_thread
               70  CALL_FUNCTION_0       0  ''
               72  LOAD_ATTR                will_stop
            74_76  POP_JUMP_IF_TRUE    666  'to 666'

 L. 749        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _input_topics
               82  POP_JUMP_IF_TRUE    114  'to 114'

 L. 750        84  LOAD_FAST                'self'
               86  LOAD_ATTR                logger
               88  LOAD_ATTR                log
               90  LOAD_STR                 'No input topics, waiting...'
               92  LOAD_STR                 'debug'
               94  LOAD_CONST               ('level',)
               96  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               98  POP_TOP          

 L. 751       100  LOAD_GLOBAL              time
              102  LOAD_METHOD              sleep
              104  LOAD_GLOBAL              Link
              106  LOAD_ATTR                TIMEOUT
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 752       112  CONTINUE             68  'to 68'
            114_0  COME_FROM            82  '82'

 L. 754       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _input_topics_lock
              118  SETUP_WITH          144  'to 144'
              120  POP_TOP          

 L. 755       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _set_input_topic_assignments
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          

 L. 756       130  LOAD_GLOBAL              dict
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _input_topic_assignments
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'current_input_topic_assignments'
              140  POP_BLOCK        
              142  LOAD_CONST               None
            144_0  COME_FROM_WITH      118  '118'
              144  WITH_CLEANUP_START
              146  WITH_CLEANUP_FINISH
              148  END_FINALLY      

 L. 758   150_152  SETUP_LOOP          664  'to 664'
              154  LOAD_FAST                'current_input_topic_assignments'
              156  LOAD_METHOD              keys
              158  CALL_METHOD_0         0  ''
              160  GET_ITER         
          162_164  FOR_ITER            662  'to 662'
              166  STORE_FAST               'topic'

 L. 760       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _input_topics_lock
              172  SETUP_WITH          194  'to 194'
              174  POP_TOP          

 L. 761       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _changed_input_topics
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L. 762       182  LOAD_CONST               False
              184  LOAD_FAST                'self'
              186  STORE_ATTR               _changed_input_topics

 L. 763       188  BREAK_LOOP       
            190_0  COME_FROM           180  '180'
              190  POP_BLOCK        
              192  LOAD_CONST               None
            194_0  COME_FROM_WITH      172  '172'
              194  WITH_CLEANUP_START
              196  WITH_CLEANUP_FINISH
              198  END_FINALLY      

 L. 765       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _input_mode
              204  LOAD_STR                 'exp'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   218  'to 218'

 L. 766       210  LOAD_FAST                'topic'
              212  BUILD_LIST_1          1 
              214  STORE_FAST               'subscription'
              216  JUMP_FORWARD        250  'to 250'
            218_0  COME_FROM           208  '208'

 L. 767       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _input_mode
              222  LOAD_STR                 'parity'
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   240  'to 240'

 L. 768       228  LOAD_GLOBAL              list
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                _input_topics
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'subscription'
              238  JUMP_FORWARD        250  'to 250'
            240_0  COME_FROM           226  '226'

 L. 770       240  LOAD_FAST                'self'
              242  LOAD_METHOD              suicide
              244  LOAD_STR                 'Unknown priority mode'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
            250_0  COME_FROM           238  '238'
            250_1  COME_FROM           216  '216'

 L. 773       250  LOAD_FAST                'consumer'
              252  LOAD_METHOD              subscribe
              254  LOAD_FAST                'subscription'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L. 774       260  LOAD_FAST                'self'
              262  LOAD_ATTR                logger
              264  LOAD_METHOD              log
              266  LOAD_STR                 '[MAIN] listening on: '
              268  LOAD_FAST                'subscription'
              270  FORMAT_VALUE          0  ''
              272  BUILD_STRING_2        2 
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          

 L. 776   278_280  SETUP_EXCEPT        596  'to 596'

 L. 777       282  LOAD_GLOBAL              utils
              284  LOAD_METHOD              get_timestamp_ms
              286  CALL_METHOD_0         0  ''
              288  STORE_FAST               'start_time'

 L. 778       290  LOAD_FAST                'current_input_topic_assignments'
              292  LOAD_FAST                'topic'
              294  BINARY_SUBSCR    
              296  STORE_FAST               'assigned_time'

 L. 779       298  LOAD_CONST               False
              300  STORE_FAST               'restarted_time'

 L. 780   302_304  SETUP_LOOP          592  'to 592'
            306_0  COME_FROM           476  '476'
              306  LOAD_FAST                'assigned_time'
              308  LOAD_CONST               -1
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_TRUE    342  'to 342'

 L. 781       316  LOAD_FAST                'assigned_time'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                _exp_window_size
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_TRUE    342  'to 342'

 L. 782       328  LOAD_FAST                'self'
              330  LOAD_METHOD              _on_time
              332  LOAD_FAST                'start_time'
              334  LOAD_FAST                'assigned_time'
              336  CALL_METHOD_2         2  ''
          338_340  POP_JUMP_IF_FALSE   590  'to 590'
            342_0  COME_FROM           324  '324'
            342_1  COME_FROM           312  '312'

 L. 783       342  LOAD_GLOBAL              current_thread
              344  CALL_FUNCTION_0       0  ''
              346  LOAD_ATTR                will_stop
          348_350  POP_JUMP_IF_TRUE    590  'to 590'

 L. 785       352  LOAD_FAST                'self'
              354  LOAD_ATTR                _input_topics_lock
              356  SETUP_WITH          382  'to 382'
              358  POP_TOP          

 L. 786       360  LOAD_FAST                'current_input_topic_assignments'
              362  LOAD_FAST                'topic'
              364  BINARY_SUBSCR    
              366  STORE_FAST               'assigned_time'

 L. 789       368  LOAD_FAST                'self'
              370  LOAD_ATTR                _changed_input_topics
          372_374  POP_JUMP_IF_FALSE   378  'to 378'

 L. 792       376  BREAK_LOOP       
            378_0  COME_FROM           372  '372'
              378  POP_BLOCK        
              380  LOAD_CONST               None
            382_0  COME_FROM_WITH      356  '356'
              382  WITH_CLEANUP_START
              384  WITH_CLEANUP_FINISH
              386  END_FINALLY      

 L. 794       388  LOAD_FAST                'consumer'
              390  LOAD_METHOD              poll
              392  LOAD_GLOBAL              Link
              394  LOAD_ATTR                TIMEOUT
              396  CALL_METHOD_1         1  ''
              398  STORE_FAST               'message'

 L. 796       400  LOAD_FAST                'message'
          402_404  POP_JUMP_IF_FALSE   426  'to 426'
              406  LOAD_FAST                'message'
              408  LOAD_METHOD              key
              410  CALL_METHOD_0         0  ''
          412_414  POP_JUMP_IF_TRUE    444  'to 444'
              416  LOAD_FAST                'message'
              418  LOAD_METHOD              value
              420  CALL_METHOD_0         0  ''
          422_424  POP_JUMP_IF_TRUE    444  'to 444'
            426_0  COME_FROM           402  '402'

 L. 797       426  LOAD_FAST                'self'
              428  LOAD_METHOD              _break_consumer_loop
              430  LOAD_FAST                'subscription'
              432  CALL_METHOD_1         1  ''
          434_436  POP_JUMP_IF_TRUE    442  'to 442'

 L. 798   438_440  CONTINUE            306  'to 306'
            442_0  COME_FROM           434  '434'

 L. 802       442  BREAK_LOOP       
            444_0  COME_FROM           422  '422'
            444_1  COME_FROM           412  '412'

 L. 804       444  LOAD_FAST                'message'
              446  LOAD_METHOD              error
              448  CALL_METHOD_0         0  ''
          450_452  POP_JUMP_IF_FALSE   516  'to 516'

 L. 806       454  LOAD_FAST                'message'
              456  LOAD_METHOD              error
              458  CALL_METHOD_0         0  ''
              460  LOAD_METHOD              code
              462  CALL_METHOD_0         0  ''
              464  LOAD_GLOBAL              KafkaError
              466  LOAD_ATTR                _PARTITION_EOF
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   498  'to 498'

 L. 807       474  LOAD_FAST                'restarted_time'
          476_478  POP_JUMP_IF_TRUE    306  'to 306'

 L. 808       480  LOAD_GLOBAL              utils
              482  LOAD_METHOD              get_timestamp_ms
              484  CALL_METHOD_0         0  ''
              486  STORE_FAST               'start_time'

 L. 809       488  LOAD_CONST               True
              490  STORE_FAST               'restarted_time'

 L. 810   492_494  CONTINUE            306  'to 306'
              496  JUMP_FORWARD        516  'to 516'
            498_0  COME_FROM           470  '470'

 L. 812       498  LOAD_FAST                'self'
              500  LOAD_METHOD              suicide
              502  LOAD_GLOBAL              str
              504  LOAD_FAST                'message'
              506  LOAD_METHOD              error
              508  CALL_METHOD_0         0  ''
              510  CALL_FUNCTION_1       1  ''
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          
            516_0  COME_FROM           496  '496'
            516_1  COME_FROM           450  '450'

 L. 815       516  LOAD_FAST                'restarted_time'
          518_520  POP_JUMP_IF_TRUE    534  'to 534'

 L. 816       522  LOAD_GLOBAL              utils
              524  LOAD_METHOD              get_timestamp_ms
              526  CALL_METHOD_0         0  ''
              528  STORE_FAST               'start_time'

 L. 817       530  LOAD_CONST               True
              532  STORE_FAST               'restarted_time'
            534_0  COME_FROM           518  '518'

 L. 820       534  LOAD_FAST                'self'
              536  LOAD_ATTR                _synchronous
          538_540  POP_JUMP_IF_FALSE   570  'to 570'

 L. 822       542  LOAD_FAST                'self'
              544  LOAD_ATTR                _input_messages
              546  LOAD_METHOD              put
              548  LOAD_FAST                'message'
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                _commit_kafka_message
              554  LOAD_FAST                'consumer'
              556  LOAD_FAST                'message'
              558  BUILD_LIST_2          2 
              560  BUILD_TUPLE_3         3 
              562  CALL_METHOD_1         1  ''
              564  POP_TOP          

 L. 823   566_568  CONTINUE            306  'to 306'
            570_0  COME_FROM           538  '538'

 L. 826       570  LOAD_FAST                'self'
              572  LOAD_ATTR                _input_messages
              574  LOAD_METHOD              put
              576  LOAD_FAST                'message'
              578  CALL_METHOD_1         1  ''
              580  POP_TOP          

 L. 827   582_584  CONTINUE            306  'to 306'
          586_588  JUMP_BACK           306  'to 306'
            590_0  COME_FROM           348  '348'
            590_1  COME_FROM           338  '338'
              590  POP_BLOCK        
            592_0  COME_FROM_LOOP      302  '302'
              592  POP_BLOCK        
              594  JUMP_BACK           162  'to 162'
            596_0  COME_FROM_EXCEPT    278  '278'

 L. 829       596  DUP_TOP          
              598  LOAD_GLOBAL              Exception
              600  COMPARE_OP               exception-match
          602_604  POP_JUMP_IF_FALSE   658  'to 658'
              606  POP_TOP          
              608  POP_TOP          
              610  POP_TOP          

 L. 830       612  SETUP_FINALLY       626  'to 626'

 L. 831       614  LOAD_FAST                'consumer'
              616  LOAD_METHOD              close
              618  CALL_METHOD_0         0  ''
              620  POP_TOP          
              622  POP_BLOCK        
              624  LOAD_CONST               None
            626_0  COME_FROM_FINALLY   612  '612'

 L. 833       626  LOAD_FAST                'self'
              628  LOAD_ATTR                logger
              630  LOAD_METHOD              log
              632  LOAD_STR                 'stopped main input'
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          

 L. 834       638  LOAD_FAST                'self'
              640  LOAD_ATTR                suicide
              642  LOAD_STR                 'Kafka consumer error'
              644  LOAD_CONST               True
              646  LOAD_CONST               ('exception',)
              648  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              650  POP_TOP          
              652  END_FINALLY      
              654  POP_EXCEPT       
              656  JUMP_BACK           162  'to 162'
            658_0  COME_FROM           602  '602'
              658  END_FINALLY      
              660  JUMP_BACK           162  'to 162'
              662  POP_BLOCK        
            664_0  COME_FROM_LOOP      150  '150'
              664  JUMP_BACK            68  'to 68'
            666_0  COME_FROM            74  '74'
              666  POP_BLOCK        
            668_0  COME_FROM_LOOP       64  '64'

 L. 836       668  LOAD_FAST                'consumer'
              670  LOAD_METHOD              close
              672  CALL_METHOD_0         0  ''
              674  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 590

    def _on_time(self, start_time, assigned_time):
        return utils.get_timestamp_ms() - start_time < 1000 * assigned_time

    def _get_index_assignment(self, index, elements_no, base=1.7):
        """
        window_size implies a full cycle consuming all the queues with
        priority.
        """
        aggregated_value = 0.0
        reverse_index = elements_no - index - 1
        for index in range(elements_no):
            value = math.pow(base, index)
            if index is reverse_index:
                index_assignment = value
            aggregated_value += value

        return index_assignment / aggregated_value * self._exp_window_size

    def _thread_target(self, target, args=None, kwargs=None):
        try:
            if args:
                target(*args)
            elif kwargs:
                target(**kwargs)
            else:
                target()
        except Exception:
            self.suicide(f'Exception during the execution of "{target.__name__}"', exception=True)

    def _loop_thread_target(self, target, args=None, kwargs=None):
        while not current_thread().will_stop:
            self._thread_target(target, args, kwargs)

    def _setup_signals_handler(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGQUIT, self._signal_handler)

    def _setup_kafka_producers(self):
        sync_producer_properties = dict(self._kafka_producer_synchronous_properties)
        self._sync_producer = Producer(sync_producer_properties)
        self.logger.log(f"sync producer properties: {utils.dump_dict_pretty(sync_producer_properties)}", level='debug')
        async_producer_properties = dict(self._kafka_producer_common_properties)
        self._async_producer = Producer(async_producer_properties)
        self.logger.log(f"async producer properties: {utils.dump_dict_pretty(async_producer_properties)}", level='debug')

    def _launch_tasks(self):
        self._generator_main_thread = Thread(target=(self._loop_thread_target), kwargs={'target': self.generator})
        self._generator_main_thread.start()
        if self._kafka_endpoint:
            producer_kwargs = {'target': self._kafka_producer}
            self._producer_thread = Thread(target=(self._thread_target), kwargs=producer_kwargs)
            self._producer_thread.start()
            self._transform_rpc_executor = ThreadPool(self, self._num_rpc_threads)
            self._transform_main_executor = ThreadPool(self, self._num_main_threads)
            transform_kwargs = {'target': self._input_handler}
            self._input_handler_thread = Thread(target=(self._thread_target), kwargs=transform_kwargs)
            self._input_handler_thread.start()
            consumer_kwargs = {'target': self._kafka_rpc_consumer}
            self._consumer_rpc_thread = Thread(target=(self._thread_target), kwargs=consumer_kwargs)
            self._consumer_rpc_thread.start()
            self._consumer_main_thread = Thread(target=(self._thread_target), kwargs={'target': self._kafka_main_consumer})
            self._consumer_main_thread.start()

    def _set_log_level(self, log_level):
        if not hasattr(self, '_log_level'):
            self._log_level = log_level.upper()

    def _set_connectors(self):
        try:
            self._aerospike = AerospikeConnector((self._aerospike_host), (self._aerospike_port), connect=True)
        except AttributeError:
            self._aerospike = None

        try:
            self._mongodb = MongodbConnector((self._mongodb_host), (self._mongodb_port), connect=True)
        except AttributeError:
            self._mongodb = None

    def _set_consumer_group(self, consumer_group, uid_consumer_group):
        if hasattr(self, 'consumer_group'):
            consumer_group = self._consumer_group
        elif hasattr(self, 'uid_consumer_group'):
            uid_consumer_group = self._uid_consumer_group
        elif uid_consumer_group:
            self._consumer_group = f"catenae_{self._uid}"
        elif consumer_group:
            self._consumer_group = consumer_group
        else:
            self._consumer_group = f"catenae_{self.__class__.__name__.lower()}"
        self.logger.log(f"consumer_group: {self._consumer_group}")

    def _set_kafka_common_properties(self):
        common_properties = {'bootstrap.servers':self._kafka_endpoint, 
         'compression.codec':'snappy', 
         'api.version.request':True}
        self._kafka_consumer_common_properties = dict(common_properties)
        self._kafka_consumer_common_properties.update({'max.partition.fetch.bytes':1048576, 
         'metadata.max.age.ms':10000, 
         'socket.receive.buffer.bytes':0, 
         'group.id':self._consumer_group, 
         'session.timeout.ms':10000, 
         'max.poll.interval.ms':self._consumer_timeout, 
         'enable.auto.commit':True, 
         'auto.commit.interval.ms':5000, 
         'default.topic.config':{'auto.offset.reset': 'smallest'}})
        self._kafka_consumer_synchronous_properties = dict(self._kafka_consumer_common_properties)
        self._kafka_consumer_synchronous_properties.update({'enable.auto.commit':False,  'auto.commit.interval.ms':0})
        self._kafka_producer_common_properties = dict(common_properties)
        self._kafka_producer_common_properties.update({'partition.assignment.strategy':'roundrobin', 
         'message.max.bytes':1048576, 
         'socket.send.buffer.bytes':0, 
         'acks':1, 
         'message.send.max.retries':10, 
         'queue.buffering.max.ms':1, 
         'max.in.flight.requests.per.connection':1, 
         'batch.num.messages':1})
        self._kafka_producer_synchronous_properties = dict(self._kafka_producer_common_properties)
        self._kafka_producer_synchronous_properties.update({'message.send.max.retries':10000000, 
         'acks':'all', 
         'max.in.flight.requests.per.connection':1, 
         'batch.num.messages':1, 
         'enable.idempotence':True})

    def _set_input_topic_assignments(self):
        if self._input_mode == 'parity':
            self._input_topic_assignments = {-1: -1}
        elif self._input_mode == 'exp':
            self._input_topic_assignments = {}
            if len(self._input_topics[0]) == 1:
                self._input_topic_assignments[self._input_topics[0]] = -1
            topics_no = len(self._input_topics)
            self.logger.log('input topics time assingments:', level='debug')
            for index, topic in enumerate(self._input_topics):
                topic_assingment = self._get_index_assignment(index, topics_no)
                self._input_topic_assignments[topic] = topic_assingment
                self.logger.log(f" * {topic}: {topic_assingment} seconds", level='debug')

    def _load_args(self):
        parser = argparse.ArgumentParser()
        Link._parse_catenae_args(parser)
        Link._parse_kafka_args(parser)
        Link._parse_aerospike_args(parser)
        Link._parse_mongodb_args(parser)
        parsed_args = parser.parse_known_args()
        link_args = parsed_args[0]
        self._args = parsed_args[1]
        self._set_catenae_properties_from_args(link_args)
        self._set_kafka_properties_from_args(link_args)
        self._set_aerospike_properties(link_args.aerospike_endpoint)
        self._set_mongodb_properties(link_args.mongodb_endpoint)

    @staticmethod
    def _parse_catenae_args(parser):
        parser.add_argument('--log-level', action='store',
          dest='log_level',
          help='Catenae log level [debug|info|warning|error|critical].',
          required=False)
        parser.add_argument('--input-mode', action='store',
          dest='input_mode',
          help='Link input mode [parity|exp].',
          required=False)
        parser.add_argument('--exp-window-size', action='store',
          dest='exp_window_size',
          help='Consumption window size in seconds for exp mode.',
          required=False)
        parser.add_argument('--sync', action='store_true',
          dest='synchronous',
          help='Synchronous mode is enabled.',
          required=False)
        parser.add_argument('--seq', action='store_true',
          dest='sequential',
          help='Sequential mode is enabled.',
          required=False)
        parser.add_argument('--random-consumer-group', action='store_true',
          dest='uid_consumer_group',
          help='Synchronous mode is disabled.',
          required=False)
        parser.add_argument('--rpc-threads', action='store',
          dest='num_rpc_threads',
          help='Number of RPC threads.',
          required=False)
        parser.add_argument('--main-threads', action='store',
          dest='num_main_threads',
          help='Number of main threads.',
          required=False)

    @staticmethod
    def _parse_kafka_args(parser):
        parser.add_argument('-i', '--input',
          action='store',
          dest='input_topics',
          help='Kafka input topics. Several topics can be specified separated by commas',
          required=False)
        parser.add_argument('-o', '--output',
          action='store',
          dest='output_topics',
          help='Kafka output topics. Several topics can be specified separated by commas',
          required=False)
        parser.add_argument('-k', '--kafka-bootstrap-server',
          action='store',
          dest='kafka_endpoint',
          help='Kafka bootstrap server.                             E.g., "localhost:9092"',
          required=False)
        parser.add_argument('-g', '--consumer-group',
          action='store',
          dest='consumer_group',
          help='Kafka consumer group.',
          required=False)
        parser.add_argument('--consumer-timeout', action='store',
          dest='consumer_timeout',
          help='Kafka consumer timeout in seconds.',
          required=False)

    @staticmethod
    def _parse_aerospike_args(parser):
        parser.add_argument('-a', '--aerospike',
          '--aerospike-bootstrap-server',
          action='store',
          dest='aerospike_endpoint',
          help='Aerospike bootstrap server.                             E.g., "localhost:3000"',
          required=False)

    @staticmethod
    def _parse_mongodb_args(parser):
        parser.add_argument('-m', '--mongodb',
          action='store',
          dest='mongodb_endpoint',
          help='MongoDB server.                             E.g., "localhost:27017"',
          required=False)

    def _set_catenae_properties_from_args(self, args):
        if args.log_level:
            self._log_level = args.log_level
        if args.input_mode:
            self._input_mode = args.input_mode
        if args.exp_window_size:
            self._exp_window_size = args.exp_window_size
        if args.synchronous:
            self._synchronous = True
        if args.sequential:
            self._sequential = True
        if args.uid_consumer_group:
            self._uid_consumer_group = True
        if args.num_rpc_threads:
            self._num_rpc_threads = args.num_rpc_threads
        if args.num_main_threads:
            self._num_main_threads = args.num_main_threads

    def _set_kafka_properties_from_args(self, args):
        if args.input_topics:
            self._input_topics = args.input_topics.split(',')
        else:
            self._input_topics = []
        if args.output_topics:
            self._output_topics = args.output_topics.split(',')
        else:
            self._output_topics = []
        self._kafka_endpoint = args.kafka_endpoint
        if args.consumer_group:
            self._consumer_group = args.consumer_group
        if args.consumer_timeout:
            self._consumer_timeout = args.consumer_timeout

    def _set_aerospike_properties(self, aerospike_endpoint):
        if aerospike_endpoint is None:
            return
        else:
            host_port = aerospike_endpoint.split(':')
            if not hasattr(self, '_aerospike_host'):
                self._aerospike_host = host_port[0]
            self._aerospike_port = hasattr(self, '_aerospike_port') or int(host_port[1])

    def _set_mongodb_properties(self, mongodb_endpoint):
        if mongodb_endpoint is None:
            return
        else:
            host_port = mongodb_endpoint.split(':')
            if not hasattr(self, '_mongodb_host'):
                self._mongodb_host = host_port[0]
            self._mongodb_port = hasattr(self, '_mongodb_port') or int(host_port[1])