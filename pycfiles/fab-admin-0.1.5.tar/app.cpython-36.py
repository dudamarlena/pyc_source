# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\opt\private\cw1427\fab-admin\fab_admin\fab_manager_overwrite\flask_rq2/app.py
# Compiled at: 2019-05-31 22:07:45
# Size of source mod 2**32: 12566 bytes
"""
    flask_rq2.app
    ~~~~~~~~~~~~~

    The core interface of Flask-RQ2.

"""
import warnings
from rq.queue import Queue
from rq.utils import import_attribute
from rq.worker import DEFAULT_RESULT_TTL
try:
    import click
except ImportError:
    click = None

class RQ(object):
    __doc__ = '\n    The main RQ object to be used in user apps.\n    '
    default_queue = 'default'
    default_timeout = Queue.DEFAULT_TIMEOUT
    default_result_ttl = DEFAULT_RESULT_TTL
    redis_url = 'redis://localhost:6379/0'
    connection_class = 'redis.StrictRedis'
    queues = [
     default_queue]
    queue_class = 'rq.queue.Queue'
    worker_class = 'rq.worker.Worker'
    job_class = 'flask_rq2.job.FlaskJob'
    scheduler_class = 'flask_rq2.scheduler.FlaskScheduler'
    scheduler_queue = default_queue
    scheduler_interval = 60
    functions_class = 'flask_rq2.functions.JobFunctions'

    def __init__(self, app=None, default_timeout=None, is_async=None, **kwargs):
        """
        Initialize the RQ interface.

        :param app: Flask application
        :type app: :class:`flask.Flask`
        :param default_timeout: The default timeout in seconds to use for jobs,
                                defaults to RQ's default of 180 seconds per job
        :type default_timeout: int
        :param is_async: Whether or not to run jobs asynchronously or
                         in-process, defaults to ``True``
        :type is_async: bool
        """
        if default_timeout is not None:
            self.default_timeout = default_timeout
        else:
            self._is_async = is_async
            if 'async' in kwargs:
                self._is_async = kwargs['async']
                warnings.warn('The `async` keyword is deprecated. Use `is_async` instead', DeprecationWarning)
            self._jobs = []
            self._exception_handlers = []
            self._queue_instances = {}
            self._functions_cls = import_attribute(self.functions_class)
            self._ready_to_connect = False
            self._connection = kwargs.get('client', None)
            if app is not None:
                self.init_app(app)

    @property
    def connection(self):
        if not self._ready_to_connect:
            raise RuntimeError('Flask-RQ2 is not ready yet to connect to Redis. Was it initialized with a Flask app?')
        if self._connection is None:
            self._connection = self._connect()
        return self._connection

    def _connect(self):
        connection_class = import_attribute(self.connection_class)
        return connection_class.from_url(self.redis_url)

    def init_app(self, app):
        """
        Initialize the app, e.g. can be used if factory pattern is used.
        """
        self.redis_url = app.config.setdefault('RQ_REDIS_URL', self.redis_url)
        self.connection_class = app.config.setdefault('RQ_CONNECTION_CLASS', self.connection_class)
        self._ready_to_connect = True
        self.queues = app.config.setdefault('RQ_QUEUES', self.queues)
        self.queue_class = app.config.setdefault('RQ_QUEUE_CLASS', self.queue_class)
        self.worker_class = app.config.setdefault('RQ_WORKER_CLASS', self.worker_class)
        self.job_class = app.config.setdefault('RQ_JOB_CLASS', self.job_class)
        self.scheduler_class = app.config.setdefault('RQ_SCHEDULER_CLASS', self.scheduler_class)
        self.scheduler_queue = app.config.setdefault('RQ_SCHEDULER_QUEUE', self.scheduler_queue)
        self.scheduler_interval = app.config.setdefault('RQ_SCHEDULER_INTERVAL', self.scheduler_interval)
        _async = app.config.setdefault('RQ_ASYNC', True)
        if self._is_async is None:
            self._is_async = _async
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['rq2'] = self
        if hasattr(app, 'cli'):
            self.init_cli(app)

    def init_cli(self, app):
        """
        Initialize the Flask CLI support in case it was enabled for the
        app.

        Works with both Flask>=1.0's CLI support as well as the backport
        in the Flask-CLI package for Flask<1.0.
        """
        if click is None:
            raise RuntimeError('Cannot import click. Is it installed?')
        from .cli import add_commands
        add_commands(app.cli, self)

    def exception_handler(self, callback):
        """
        Decorator to add an exception handler to the worker, e.g.::

            rq = RQ()

            @rq.exception_handler
            def my_custom_handler(job, *exc_info):
                # do custom things here
                ...

        """
        path = '.'.join([callback.__module__, callback.__name__])
        self._exception_handlers.append(path)
        return callback

    def job(self, func_or_queue=None, timeout=None, result_ttl=None, ttl=None, depends_on=None, at_front=None, meta=None, description=None):
        """
        Decorator to mark functions for queuing via RQ, e.g.::

            rq = RQ()

            @rq.job
            def add(x, y):
                return x + y

        or::

            @rq.job(timeout=60, result_ttl=60 * 60)
            def add(x, y):
                return x + y

        Adds various functions to the job as documented in
        :class:`~flask_rq2.functions.JobFunctions`.

        .. versionchanged:: 18.0
            Adds ``depends_on``, ``at_front``, ``meta`` and ``description``
            parameters.

        :param queue: Name of the queue to add job to, defaults to
                      :attr:`flask_rq2.app.RQ.default_queue`.
        :type queue: str
        :param timeout: The maximum runtime in seconds of the job before it's
                        considered 'lost', defaults to 180.
        :type timeout: int
        :param result_ttl: Time to persist the job results in Redis,
                           in seconds.
        :type result_ttl: int
        :param ttl: The maximum queued time of the job before it'll be
                    cancelled.
        :type ttl: int

        :param depends_on: A job instance or id that the new job depends on.
        :type depends_on: ~flask_rq2.job.FlaskJob or str

        :param at_front: Whether or not the job is queued in front of all other
                         enqueued jobs.
        :type at_front: bool

        :param meta: Additional meta data about the job.
        :type meta: dict

        :param description: Description of the job.
        :type description: str

        """
        if callable(func_or_queue):
            func = func_or_queue
            queue_name = None
        else:
            func = None
            queue_name = func_or_queue

        def wrapper(wrapped):
            self._jobs.append(wrapped)
            helper = self._functions_cls(rq=self,
              wrapped=wrapped,
              queue_name=queue_name,
              timeout=timeout,
              result_ttl=result_ttl,
              ttl=ttl,
              depends_on=depends_on,
              at_front=at_front,
              meta=meta,
              description=description)
            wrapped.helper = helper
            for function in helper.functions:
                callback = getattr(helper, function, None)
                setattr(wrapped, function, callback)

            return wrapped

        if func is None:
            return wrapper
        else:
            return wrapper(func)

    def get_scheduler(self, interval=None, queue=None):
        """
        When installed returns a ``rq_scheduler.Scheduler`` instance to
        schedule job execution, e.g.::

            scheduler = rq.get_scheduler(interval=10)

        :param interval: Time in seconds of the periodic check for scheduled
                         jobs.
        :type interval: int
        :param queue: Name of the queue to enqueue in, defaults to
                     :attr:`~flask_rq2.RQ.scheduler_queue`.
        :type queue: str
        """
        if interval is None:
            interval = self.scheduler_interval
        if not queue:
            queue = self.scheduler_queue
        scheduler_cls = import_attribute(self.scheduler_class)
        scheduler = scheduler_cls(queue_name=queue,
          interval=interval,
          connection=(self.connection))
        return scheduler

    def get_queue(self, name=None):
        """
        Returns an RQ queue instance with the given name, e.g.::

            default_queue = rq.get_queue()
            low_queue = rq.get_queue('low')

        :param name: Name of the queue to return, defaults to
                     :attr:`~flask_rq2.RQ.default_queue`.
        :type name: str
        :return: An RQ queue instance.
        :rtype: ``rq.queue.Queue``
        """
        if not name:
            name = self.default_queue
        queue = self._queue_instances.get(name)
        if queue is None:
            queue_cls = import_attribute(self.queue_class)
            queue = queue_cls(name=name,
              default_timeout=(self.default_timeout),
              is_async=(self._is_async),
              connection=(self.connection),
              job_class=(self.job_class))
            self._queue_instances[name] = queue
        return queue

    def get_worker(self, *queues):
        r"""
        Returns an RQ worker instance for the given queue names, e.g.::

            configured_worker = rq.get_worker()
            default_worker = rq.get_worker('default')
            default_low_worker = rq.get_worker('default', 'low')

        :param \*queues: Names of queues the worker should act on, falls back
                          to the configured queues.
        """
        if not queues:
            queues = self.queues
        queues = [self.get_queue(name) for name in queues]
        worker_cls = import_attribute(self.worker_class)
        worker = worker_cls(queues,
          connection=(self.connection),
          job_class=(self.job_class),
          queue_class=(self.queue_class))
        for exception_handler in self._exception_handlers:
            worker.push_exc_handler(import_attribute(exception_handler))

        return worker