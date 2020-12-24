# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/viator/coding/code/microservices/microservices/queues/service.py
# Compiled at: 2018-08-29 11:19:35
# Size of source mod 2**32: 13864 bytes
import socket
from multiprocessing.pool import ThreadPool
from time import sleep
import six
from kombu import Connection, Consumer, Queue
from kombu.exceptions import MessageStateError
from kombu.utils import nested
from microservices.helpers.logs import InstanceLogger
from microservices.utils import get_logger
_logger = get_logger(__name__)

class HandlerError(Exception):
    pass


class DeferredMessage(object):
    _methods_for_callbacks = {
     'ack', 'reject', 'requeue', 'reject_log_error',
     'ack_log_error'}

    def __init__(self, message, deferred_callbacks):
        self.message = message
        self.deferred_callbacks = deferred_callbacks

    @property
    def with_deferred_callbacks(self):
        return self.deferred_callbacks is not None

    def __getattr__(self, item):
        entity = getattr(self.message, item)
        if self.with_deferred_callbacks:
            if item in self._methods_for_callbacks:
                return lambda *args**args: self.deferred_callbacks.append(lambda : entity(*args, **kwargs))
            else:
                return entity
        else:
            return entity


@six.python_2_unicode_compatible
class Rule(object):
    """Rule"""

    def __init__(self, name, handler, logger, autoack=True, deferred_callbacks=None, pool=None, **options):
        """Initialization

        :param name: name of queue
        :param handler: handle for queue
        :param autoack: if true, call message.ack()
        """
        self.handler = handler
        self.name = name
        self.options = options
        self.autoack = autoack
        self.logger = InstanceLogger(self, logger)
        self._name = '<queue: {}>'.format(self.name)
        self.deferred_callbacks = deferred_callbacks
        self.pool = pool

    def __str__(self):
        return self._name

    @property
    def with_deferred_callbacks(self):
        return self.deferred_callbacks is not None

    def add_to_pool(self, handler):
        self.pool.apply_async(handler)

    def callback(self, body, message):
        message = DeferredMessage(message, self.deferred_callbacks)
        self.logger.debug('Data (len: %s) received', len(body))

        def autoack():
            try:
                self.logger.debug('Ack message via autoack')
                message.ack()
            except ConnectionError as e:
                self.logger.error('Connection error: %s when try message.ack', e.strerror)
            except MessageStateError:
                self.logger.warning('ACK() was called in handler?')

        def handler():
            try:
                self.logger.debug('Call handler...')
                self.handler(body, HandlerContext(message, self))
            except Exception:
                self.logger.exception('Something happened in user handler')
                raise HandlerError('Something happened in user handler')

            if self.autoack:
                autoack()

        if self.with_deferred_callbacks:
            self.logger.debug('Add handler to pool')
            self.add_to_pool(handler)
        else:
            handler()


class HandlerContext(object):
    __doc__ = 'Context for handler function'

    def __init__(self, message, rule):
        """Initialization

        :param message: original message from kombu
        :type message: kombu.Message
        :param rule: rule object
        :type rule: Rule
        """
        self.message = message
        self.rule = rule


@six.python_2_unicode_compatible
class Microservice(object):
    __doc__ = 'Microservice for queues'
    connection = 'amqp:///'

    def __init__(self, connection='amqp:///', logger=None, timeout=1, name=None, workers=None, pool_factory=ThreadPool, reconnect_timeout=1, reconnect_enable=True, workers_override_prefetch=True, immediate_connect=True):
        """Initialization

        :type pool_factory: callable object, pool should has property size
        :param pool_factory: for pool will by configurated as pool_factory(workers)
        :type workers: int
        :param workers: count of workers in pool
        :param connection: connection for queues broker
        :type connection: str, None, dict or Connection
        :param logger: logging instance
        :type logger: Logger
        :param timeout: sleeping for loop, default = 0.1
        :type timeout: None, int or float
        """
        if logger is None:
            logger = _logger
        self.logger = InstanceLogger(self, logger)
        self.connection = self._get_connection(connection)
        self.timeout = timeout
        self.consumers = []
        self.reconnect_timeout = reconnect_timeout
        self.reconnect_enable = reconnect_enable
        self.workers_override_prefetch = workers_override_prefetch
        if name is None:
            try:
                name = '<microservice: {}>'.format(self.connection.as_uri())
            except:
                name = '<microservice: {}>'.format(self.connection.transport_cls)

        self.name = name
        self._stop = False
        self._stopped = False
        self.pool = None
        self.workers = workers
        self.deferred_callbacks = None
        if workers:
            self.deferred_callbacks = []
            self.pool = pool_factory(workers)
        if immediate_connect:
            self.connect()

    def __str__(self):
        return self.name

    @property
    def with_pool(self):
        return self.pool is not None

    def _get_connection(self, connection):
        """Create connection strategy

        :param connection: connection for broker
        :type connection: str, None, kombu.connections.Connection, dict
        :return: instance of kombu.connections.Connection
        :rtype: Connection
        """
        if not connection:
            connection = self.connection
        if isinstance(connection, str):
            connection = {'hostname': connection}
        if isinstance(connection, dict):
            connection = Connection(**connection)
        return connection

    def add_queue_rule(self, handler, name, autoack=True, prefetch_size=0, prefetch_count=0, **kwargs):
        """Add queue rule to Microservice

        :param prefetch_count: count of messages for getting from mq
        :param prefetch_size: size in bytes for getting data from mq
        :param handler: function for handling messages
        :param autoack: if True message.ack() after callback
        :type handler: callable object
        :param name: name of queue
        :type name: str
        """
        if self.with_pool:
            if self.workers_override_prefetch:
                prefetch_count = self.workers
            rule = Rule(name, handler, self.logger, autoack=autoack, deferred_callbacks=self.deferred_callbacks, pool=self.pool, **kwargs)
        else:
            rule = Rule(name, handler, self.logger, autoack=autoack, **kwargs)
        self.connect()
        consumer = Consumer(self.connection, queues=[Queue(rule.name)], callbacks=[
         rule.callback], auto_declare=True)
        consumer.qos(prefetch_count=prefetch_count, prefetch_size=prefetch_size)
        self.consumers.append(consumer)
        self.logger.debug('Rule "%s" added!', rule.name)

    def _start(self):
        self._stopped = False
        self._stop = False
        self.connect()

    def stop(self):
        self._stop = True
        self.logger.info('Try to stop microservice draining events')

    def queue(self, name, autoack=True, prefetch_size=0, prefetch_count=0, **kwargs):
        """Decorator for handler function

        >>>app = Microservice()
        >>>
        >>>@app.queue('queue')
        >>>def function(payload, context):
        >>>    pass

        :param prefetch_count: count of messages for getting from mq
        :param prefetch_size: size in bytes for getting data from mq
        :param autoack: if True message.ack() after callback
        :param name: name of queue
        :type name: str
        """

        def decorator(f):
            self.add_queue_rule(f, name, autoack=autoack, prefetch_size=prefetch_size, prefetch_count=prefetch_count, **kwargs)
            return f

        return decorator

    def connect(self):
        """Try connect to mq"""
        while not self._stop and not self.connection.connected:
            try:
                self.connection.connect()
                self.logger.info('Connected to mq broker')
                break
            except ConnectionError as e:
                if self.reconnect_enable:
                    self.logger.error('Connection error, cause: %s. Reconnecting...', e.strerror)
                else:
                    self.stop()
                    break
            except Exception:
                self.logger.exception('Error when try to connect')

            sleep(self.reconnect_timeout)

    def revive(self):

        def _revive():
            for i, consumer in enumerate(self.consumers):
                self.logger.debug('Try revive consumer: %s', i)
                consumer.channel = self.connection
                consumer.revive(consumer.channel)
                self.logger.debug('Consumer: %s was revived', i)

        while not self._stop:
            try:
                _revive()
                break
            except ConnectionError:
                if self.reconnect_enable:
                    self.connect()
                else:
                    self.stop()
                    break
            except Exception:
                self.logger.exception('Error when try to revive')
                sleep(self.reconnect_timeout)

        self.logger.debug('All consumers %s was revived...', len(self.consumers))

    @property
    def stopped(self):
        return self._stopped

    def drain_results(self):
        while self.deferred_callbacks:
            callback = self.deferred_callbacks.pop()
            try:
                callback()
                self.logger.debug('Called callback. All: %s', len(self.deferred_callbacks))
            except ConnectionError as e:
                self.logger.error('Connection error when try callback: %s. Cause: %s. Message will be handled on next iteration', callback, e.strerror)
            except Exception:
                self.logger.exception('Unknown exception when try callback: %s', callback)

    def drain_events(self, infinity=True):
        with nested(*self.consumers):
            while not self._stop:
                try:
                    self.connection.drain_events(timeout=self.timeout)
                except socket.timeout:
                    if not infinity:
                        break
                except ConnectionError as e:
                    self.logger.error('Connection to mq has broken off because: %s. Try to reconnect, %s', e)
                    self.connect()
                    self.revive()
                    break
                except HandlerError:
                    self.logger.exception('Handler error')
                except Exception as e:
                    if not self._stop:
                        self.logger.exception('Something wrong! Try to restart the loop')
                        self.revive()
                        break
                    else:
                        self.logger.exception('Something wrong! And stopping...')
                        break

                if self.with_pool:
                    try:
                        self.drain_results()
                    except Exception:
                        self.logger.exception('Unknown error when draining results')

        if self._stop:
            if self.with_pool:
                try:
                    self.pool.join()
                    self.drain_results()
                except AssertionError:
                    pass
                except Exception:
                    self.logger.exception('Unknown error when draining results')

                self._stopped = True
                self.logger.info('Stopped draining events.')

    def run(self, debug=False):
        """Run microservice in loop, where handle connections

        :param debug: enable/disable debug mode
        :type debug: bool
        """
        if debug:
            from microservices.utils import set_logging
            set_logging('DEBUG')

        def _run():
            self._start()
            self.drain_events(infinity=True)

        while not self._stopped:
            _run()

    def read(self, count=1):
        for x in range(count):
            self.drain_events(infinity=False)