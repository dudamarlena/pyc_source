# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/log/middleware.py
# Compiled at: 2006-08-02 05:57:50
import time
from harold.lib import mapping_response_hook, header_match
default_format = '%h %l %u %t "%r" %>s %b'
default_value = '-'
arg_pat = '%(?:\\{(?P<arg>.*?)\\})*?'

def remote_host(app, info, res, env):
    return env.get('REMOTE_ADDR', default_value)


def remote_log(app, info, res, env):
    return default_value


def remote_user(app, info, res, env):
    return env.get('REMOTE_USER', default_value)


def received_time(app, info, res, env):
    return time.ctime(env.get('requestlog.start', default_value))


def first_request_line(app, info, res, env):
    return '%s %s' % (env['REQUEST_METHOD'], env.get('SCRIPT_NAME', '') + env['PATH_INFO'] or '/')


def first_response(app, info, res, env):
    return info['status'].split(' ')[0]


def last_response(app, info, res, env):
    return info['status'].split(' ')[0]


def response_size(app, info, res, env):
    try:
        return len(res)
    except:
        return -1


replacers = {'%h': remote_host, '%l': remote_log, '%u': remote_user, '%t': received_time, '%r': first_request_line, '%s': first_response, '%>s': last_response, '%b': response_size}
from harold.log import logger

class RequestLog:
    __module__ = __name__

    def __init__(self, app, format=None):
        self.app = app
        if format is None:
            format = default_format
        self.format = format
        self.log = logger(self)
        return

    def __call__(self, environ, start_response):
        environ['requestlog.start'] = time.time()
        response_info = {}
        mapping_response = mapping_response_hook(start_response, response_info)
        response = self.app(environ, mapping_response)
        message = self.message(response_info, response, environ)
        self.log.debug(message)
        return response

    def message(self, mapping, data, env):
        msg = self.format
        for (key, value) in replacers.items():
            msg = msg.replace(key, str(value(self, mapping, data, env)))

        return msg