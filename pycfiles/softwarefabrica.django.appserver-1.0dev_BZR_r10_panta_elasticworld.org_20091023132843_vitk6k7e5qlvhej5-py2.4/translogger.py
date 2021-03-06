# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/appserver/translogger.py
# Compiled at: 2009-02-25 15:48:51
"""
Middleware for logging requests, using Apache combined log format
"""
import logging, time, urllib

class TransLogger(object):
    """
    This logging middleware will log all requests as they go through.
    They are, by default, sent to a logger named ``'wsgi'`` at the
    INFO level.

    If ``setup_console_handler`` is true, then messages for the named
    logger will be sent to the console.
    """
    __module__ = __name__
    format = '%(REMOTE_ADDR)s - %(REMOTE_USER)s [%(time)s] "%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" %(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'

    def __init__(self, application, logger=None, format=None, logging_level=logging.INFO, logger_name='wsgi', setup_console_handler=True, set_logger_level=logging.DEBUG):
        if format is not None:
            self.format = format
        self.application = application
        self.logging_level = logging_level
        self.logger_name = logger_name
        if logger is None:
            self.logger = logging.getLogger(self.logger_name)
            if setup_console_handler:
                console = logging.StreamHandler()
                console.setLevel(logging.DEBUG)
                console.setFormatter(logging.Formatter('%(message)s'))
                self.logger.addHandler(console)
                self.logger.propagate = False
            if set_logger_level is not None:
                self.logger.setLevel(set_logger_level)
        else:
            self.logger = logger
        return

    def __call__(self, environ, start_response):
        start = time.localtime()
        req_uri = urllib.quote(environ.get('SCRIPT_NAME', '') + environ.get('PATH_INFO', ''))
        if environ.get('QUERY_STRING'):
            req_uri += '?' + environ['QUERY_STRING']
        method = environ['REQUEST_METHOD']

        def replacement_start_response(status, headers, exc_info=None):
            bytes = None
            for (name, value) in headers:
                if name.lower() == 'content-length':
                    bytes = value

            self.write_log(environ, method, req_uri, start, status, bytes)
            return start_response(status, headers)

        return self.application(environ, replacement_start_response)

    def write_log(self, environ, method, req_uri, start, status, bytes):
        if bytes is None:
            bytes = '-'
        if time.daylight:
            offset = time.altzone / 60 / 60 * -100
        else:
            offset = time.timezone / 60 / 60 * -100
        if offset >= 0:
            offset = '+%0.4d' % offset
        elif offset < 0:
            offset = '%0.4d' % offset
        d = {'REMOTE_ADDR': environ.get('REMOTE_ADDR') or '-', 'REMOTE_USER': environ.get('REMOTE_USER') or '-', 'REQUEST_METHOD': method, 'REQUEST_URI': req_uri, 'HTTP_VERSION': environ.get('SERVER_PROTOCOL'), 'time': time.strftime('%d/%b/%Y:%H:%M:%S ', start) + offset, 'status': status.split(None, 1)[0], 'bytes': bytes, 'HTTP_REFERER': environ.get('HTTP_REFERER', '-'), 'HTTP_USER_AGENT': environ.get('HTTP_USER_AGENT', '-')}
        message = self.format % d
        self.logger.log(self.logging_level, message)
        return


def make_filter(app, global_conf, logger_name='wsgi', format=None, logging_level=logging.INFO, setup_console_handler=True, set_logger_level=logging.DEBUG):
    from paste.util.converters import asbool
    if isinstance(logging_level, basestring):
        logging_level = logging._levelNames[logging_level]
    if isinstance(set_logger_level, basestring):
        set_logger_level = logging._levelNames[set_logger_level]
    return TransLogger(app, format=format or None, logging_level=logging_level, logger_name=logger_name, setup_console_handler=asbool(setup_console_handler), set_logger_level=set_logger_level)


make_filter.__doc__ = TransLogger.__doc__