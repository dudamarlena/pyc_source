# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/middleware/logger.py
# Compiled at: 2009-10-14 13:31:00
"""
Logging middleware.

To use this middleware, in settings.py you need to set:

MIDDLEWARE_CLASSES = (
    ...
    'softwarefabrica.django.utils.middleware.logger.LoggingMiddleware',
    ...)

You should need to keep the middleware as one of the first classes in
MIDDLEWARE_CLASSES, to be able to process logs from subsequent stages.
"""
import sys, time, re
try:
    import thread
except ImportError:
    import dummy_thread as thread

try:
    import threading
except ImportError:
    import dummy_threading as threading

import hashlib, logging
from logging import Logger
import struct
from django.conf import settings

class LoggerRequestState(threading.local):
    __module__ = __name__
    __slots__ = ('request_id', 'request')

    def __init__(self):
        self.request_id = None
        self.request = None
        return


LOGGER_DEFAULT_LEVEl = logging.INFO
if getattr(settings, 'DEBUG', False):
    LOGGER_DEFAULT_LEVEl = logging.DEBUG
LOGGER_DEFAULT_FORMAT = '[%(asctime)s %(REMOTE_ADDR)s %(request_id)s %(name)s %(levelname)s] %(message)s'
FORMAT_TOKEN_RE = re.compile('%\\(([^\\)]+)\\)s')

class RequestLogger(Logger):
    """
    Subclass of logging.Logger that adds the thread-local request info to
    the logging context. The keys available for use in the format are:

        'request_id': the unique request identifier
        'path': from request.path
        'method': from request.method

    and all the keys in request.META, so all the request headers.
    """
    __module__ = __name__

    def __init__(self, name, level=logging.NOTSET):
        global logger_config
        level = LOGGER_DEFAULT_LEVEl
        if logger_config:
            assert isinstance(logger_config, LoggerConfig)
            level = logger_config.log_level
        Logger.__init__(self, name, level=level)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        """
        Add request information to the LogRecord.

        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        r = logging.Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra)
        r.__dict__['request_id'] = getattr(logger_request_state, 'request_id', '--') or '--'
        r.__dict__['path'] = getattr(logger_request_state, 'request.path', '--')
        r.__dict__['method'] = getattr(logger_request_state, 'request.method', '--')
        if hasattr(logger_request_state, 'request') and logger_request_state.request:
            for (key, value) in logger_request_state.request.META.items():
                r.__dict__[key] = value

        format = LOGGER_DEFAULT_FORMAT
        if logger_config:
            assert isinstance(logger_config, LoggerConfig)
            format = logger_config.LOGGER_FORMAT
        for token in FORMAT_TOKEN_RE.findall(format):
            if not r.__dict__.has_key(token):
                r.__dict__[token] = '--'

        return r


class LoggerConfig(object):
    __module__ = __name__

    def __init__(self):
        self.enabled = getattr(settings, 'LOG_ENABLED', False)
        self.log_file = getattr(settings, 'LOG_FILE', None)
        self.log_file_mode = getattr(settings, 'LOG_FILE_MODE', 'a')
        self.log_stream = getattr(settings, 'LOG_STREAM', None)
        self.log_handler = getattr(settings, 'LOG_HANDLER', None)
        self.log_level = getattr(settings, 'LOG_LEVEL', LOGGER_DEFAULT_LEVEl)
        self.log_name = getattr(settings, 'LOG_NAME', 'django')
        self.log_format = getattr(settings, 'LOG_FORMAT', LOGGER_DEFAULT_FORMAT)
        self.settings_logger = getattr(settings, 'LOG_LOGGER', None)
        self.logger = None
        self.appname = getattr(settings, 'LOG_APP_NAME', None)
        if self.appname is None:
            settings_module = getattr(settings, 'SETTINGS_MODULE', 'django')
            self.appname = settings_module
            if '.' in settings_module:
                self.appname = self.appname[:self.appname.index('.')]
        self.LOGGER_FORMAT = '%s: %s' % (self.appname, self.log_format)
        if self.log_handler is None:
            if self.log_file:
                self.log_handler = logging.FileHandler(self.log_file, self.log_file_mode)
            elif self.log_stream:
                self.log_handler = logging.StreamHandler(self.log_stream)
            else:
                self.log_handler = logging.StreamHandler(sys.stderr)
        self.log_handler.setFormatter(logging.Formatter(self.LOGGER_FORMAT))
        self.log_handler.setLevel(self.log_level)
        logging.setLoggerClass(RequestLogger)
        if self.settings_logger is not None:
            logger = self.settings_logger
            logger.setLevel(self.log_level)
        else:
            logger = RequestLogger('root', self.log_level)
            logging.root = logger
            logging.root.addHandler(self.log_handler)
            logging.root.setLevel(self.log_level)
        self.logger = logger
        logging.Logger.root = logging.root
        logging.Logger.manager = logging.Manager(logging.Logger.root)
        if getattr(settings, 'DEBUG', False):
            logging.debug("logger configured; root logger: %s, level: %s, handlers: %s, format: '%s'" % (logging.root, logging.root.getEffectiveLevel(), logging.root.handlers, self.LOGGER_FORMAT))
        return


def setup_logger_middleware():
    global logger_config
    global logger_middleware_is_setup
    if logger_middleware_is_setup:
        assert logger_config is not None
        return True
    assert logger_config is None
    logger_config = LoggerConfig()
    logger_middleware_is_setup = True
    return True


def get_logger():
    """
    Return the root logging.Logger object (RequestLogger).
    """
    if not logger_middleware_is_setup:
        setup_logger_middleware()
    if logger_config:
        assert isinstance(logger_config, LoggerConfig)
        return logger_config.logger
    return logging.root


logger_config = None
logger_request_state = LoggerRequestState()
logger_middleware_is_setup = False
setup_logger_middleware()

def get_request_id(request):
    """
    Create a unique tag for the request, to make it easier to follow its log
    entries.
    """
    request_path = request.get_full_path()
    if isinstance(request_path, unicode):
        request_path_enc = request_path.encode('utf-8')
    else:
        request_path_enc = request_path
    s = hashlib.sha1()
    s.update(str(time.time()))
    s.update(request.META['REMOTE_ADDR'])
    s.update(request.META['SERVER_NAME'])
    s.update(request_path_enc)
    h = s.hexdigest()
    l = long(h, 16)
    tag = struct.pack('d', l).encode('base64').replace('\n', '').strip('=')
    return tag


def configure(request):
    logger_request_state.request = request
    if request.META.has_key('UNIQUE_ID'):
        logger_request_state.request_id = request.META['UNIQUE_ID']
    else:
        logger_request_state.request_id = get_request_id(request)
    if logger_config:
        assert isinstance(logger_config, LoggerConfig)
        request.logger = logger_config.logger


class LoggingMiddleware(object):
    """
    LoggingMiddleware configures a logging context for each request. It
    should be installed first in your MIDDLEWARE_CLASSES setting, so that the
    request information is available to logging statements as early as
    possible.
    """
    __module__ = __name__

    def __init__(self):
        super(LoggingMiddleware, self).__init__()

    def process_request(self, request):
        configure(request)
        return

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return