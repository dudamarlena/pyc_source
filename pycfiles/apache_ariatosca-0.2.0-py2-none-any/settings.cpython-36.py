# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/settings.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11662 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import atexit, logging, os, pendulum, sys
from typing import Any
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from airflow.configuration import conf, AIRFLOW_HOME, WEBSERVER_CONFIG
from airflow.contrib.kubernetes.pod import Pod
from airflow.logging_config import configure_logging
from airflow.utils.sqlalchemy import setup_event_handlers
log = logging.getLogger(__name__)
RBAC = conf.getboolean('webserver', 'rbac')
TIMEZONE = pendulum.timezone('UTC')
try:
    tz = conf.get('core', 'default_timezone')
    if tz == 'system':
        TIMEZONE = pendulum.local_timezone()
    else:
        TIMEZONE = pendulum.timezone(tz)
except Exception:
    pass

log.info('Configured default timezone %s' % TIMEZONE)

class DummyStatsLogger(object):

    @classmethod
    def incr(cls, stat, count=1, rate=1):
        pass

    @classmethod
    def decr(cls, stat, count=1, rate=1):
        pass

    @classmethod
    def gauge(cls, stat, value, rate=1, delta=False):
        pass

    @classmethod
    def timing(cls, stat, dt):
        pass


Stats = DummyStatsLogger
if conf.getboolean('scheduler', 'statsd_on'):
    from statsd import StatsClient
    statsd = StatsClient(host=(conf.get('scheduler', 'statsd_host')),
      port=(conf.getint('scheduler', 'statsd_port')),
      prefix=(conf.get('scheduler', 'statsd_prefix')))
    Stats = statsd
else:
    Stats = DummyStatsLogger
HEADER = '\n'.join([
 '  ____________       _____________',
 ' ____    |__( )_________  __/__  /________      __',
 '____  /| |_  /__  ___/_  /_ __  /_  __ \\_ | /| / /',
 '___  ___ |  / _  /   _  __/ _  / / /_/ /_ |/ |/ /',
 ' _/_/  |_/_/  /_/    /_/    /_/  \\____/____/|__/'])
LOGGING_LEVEL = logging.INFO
GUNICORN_WORKER_READY_PREFIX = '[ready] '
LOG_FORMAT = conf.get('core', 'log_format')
SIMPLE_LOG_FORMAT = conf.get('core', 'simple_log_format')
SQL_ALCHEMY_CONN = None
DAGS_FOLDER = None
PLUGINS_FOLDER = None
LOGGING_CLASS_PATH = None
engine = None
Session = None

def policy(task_instance):
    """
    This policy setting allows altering task instances right before they
    are executed. It allows administrator to rewire some task parameters.

    Note that the ``TaskInstance`` object has an attribute ``task`` pointing
    to its related task object, that in turns has a reference to the DAG
    object. So you can use the attributes of all of these to define your
    policy.

    To define policy, add a ``airflow_local_settings`` module
    to your PYTHONPATH that defines this ``policy`` function. It receives
    a ``TaskInstance`` object and can alter it where needed.

    Here are a few examples of how this can be useful:

    * You could enforce a specific queue (say the ``spark`` queue)
        for tasks using the ``SparkOperator`` to make sure that these
        task instances get wired to the right workers
    * You could force all task instances running on an
        ``execution_date`` older than a week old to run in a ``backfill``
        pool.
    * ...
    """
    pass


def pod_mutation_hook(pod):
    """
    This setting allows altering ``Pod`` objects before they are passed to
    the Kubernetes client by the ``PodLauncher`` for scheduling.

    To define a pod mutation hook, add a ``airflow_local_settings`` module
    to your PYTHONPATH that defines this ``pod_mutation_hook`` function.
    It receives a ``Pod`` object and can alter it where needed.

    This could be used, for instance, to add sidecar or init containers
    to every worker pod launched by KubernetesExecutor or KubernetesPodOperator.
    """
    pass


def configure_vars():
    global DAGS_FOLDER
    global PLUGINS_FOLDER
    global SQL_ALCHEMY_CONN
    SQL_ALCHEMY_CONN = conf.get('core', 'SQL_ALCHEMY_CONN')
    DAGS_FOLDER = os.path.expanduser(conf.get('core', 'DAGS_FOLDER'))
    PLUGINS_FOLDER = conf.get('core',
      'plugins_folder',
      fallback=(os.path.join(AIRFLOW_HOME, 'plugins')))


def configure_orm(disable_connection_pool=False):
    global Session
    global engine
    log.debug('Setting up DB connection pool (PID %s)' % os.getpid())
    engine_args = {}
    pool_connections = conf.getboolean('core', 'SQL_ALCHEMY_POOL_ENABLED')
    if disable_connection_pool or not pool_connections:
        engine_args['poolclass'] = NullPool
        log.debug('settings.configure_orm(): Using NullPool')
    else:
        if 'sqlite' not in SQL_ALCHEMY_CONN:
            try:
                pool_size = conf.getint('core', 'SQL_ALCHEMY_POOL_SIZE')
            except conf.AirflowConfigException:
                pool_size = 5

            try:
                max_overflow = conf.getint('core', 'SQL_ALCHEMY_MAX_OVERFLOW')
            except conf.AirflowConfigException:
                max_overflow = 10

            try:
                pool_recycle = conf.getint('core', 'SQL_ALCHEMY_POOL_RECYCLE')
            except conf.AirflowConfigException:
                pool_recycle = 1800

            log.info('settings.configure_orm(): Using pool settings. pool_size={}, max_overflow={}, pool_recycle={}, pid={}'.format(pool_size, max_overflow, pool_recycle, os.getpid()))
            engine_args['pool_size'] = pool_size
            engine_args['pool_recycle'] = pool_recycle
            engine_args['max_overflow'] = max_overflow
    engine_args['encoding'] = conf.get('core', 'SQL_ENGINE_ENCODING', fallback='utf-8')
    engine_args['encoding'] = engine_args['encoding'].__str__()
    engine = create_engine(SQL_ALCHEMY_CONN, **engine_args)
    reconnect_timeout = conf.getint('core', 'SQL_ALCHEMY_RECONNECT_TIMEOUT')
    setup_event_handlers(engine, reconnect_timeout)
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
      bind=engine,
      expire_on_commit=False))


def dispose_orm():
    """ Properly close pooled database connections """
    global Session
    global engine
    log.debug('Disposing DB connection pool (PID %s)', os.getpid())
    if Session:
        Session.remove()
        Session = None
    if engine:
        engine.dispose()
        engine = None


def configure_adapters():
    from pendulum import Pendulum
    try:
        from sqlite3 import register_adapter
        register_adapter(Pendulum, lambda val: val.isoformat(' '))
    except ImportError:
        pass

    try:
        import MySQLdb.converters
        MySQLdb.converters.conversions[Pendulum] = MySQLdb.converters.DateTime2literal
    except ImportError:
        pass

    try:
        import pymysql.converters
        pymysql.converters.conversions[Pendulum] = pymysql.converters.escape_datetime
    except ImportError:
        pass


def validate_session():
    worker_precheck = conf.getboolean('core', 'worker_precheck', fallback=False)
    if not worker_precheck:
        return True
    else:
        check_session = sessionmaker(bind=engine)
        session = check_session()
        try:
            session.execute('select 1')
            conn_status = True
        except exc.DBAPIError as err:
            log.error(err)
            conn_status = False

        session.close()
        return conn_status


def configure_action_logging():
    """
    Any additional configuration (register callback) for airflow.utils.action_loggers
    module
    :rtype: None
    """
    pass


def prepare_syspath():
    """
    Ensures that certain subfolders of AIRFLOW_HOME are on the classpath
    """
    if DAGS_FOLDER not in sys.path:
        sys.path.append(DAGS_FOLDER)
    else:
        config_path = os.path.join(AIRFLOW_HOME, 'config')
        if config_path not in sys.path:
            sys.path.append(config_path)
        if PLUGINS_FOLDER not in sys.path:
            sys.path.append(PLUGINS_FOLDER)


def import_local_settings():
    try:
        import airflow_local_settings
        if hasattr(airflow_local_settings, '__all__'):
            for i in airflow_local_settings.__all__:
                globals()[i] = getattr(airflow_local_settings, i)

        else:
            for k, v in airflow_local_settings.__dict__.items():
                if not k.startswith('__'):
                    globals()[k] = v

        log.info('Loaded airflow_local_settings from ' + airflow_local_settings.__file__ + '.')
    except ImportError:
        log.debug('Failed to import airflow_local_settings.', exc_info=True)


def initialize():
    global LOGGING_CLASS_PATH
    configure_vars()
    prepare_syspath()
    import_local_settings()
    LOGGING_CLASS_PATH = configure_logging()
    configure_adapters()
    configure_orm()
    configure_action_logging()
    atexit.register(dispose_orm)


KILOBYTE = 1024
MEGABYTE = KILOBYTE * KILOBYTE
WEB_COLORS = {'LIGHTBLUE':'#4d9de0',  'LIGHTORANGE':'#FF9933'}
CONTEXT_MANAGER_DAG = None