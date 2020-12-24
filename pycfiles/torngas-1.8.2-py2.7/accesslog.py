# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/middleware/accesslog.py
# Compiled at: 2016-02-16 00:41:00
"""
access log中间件，替换tornado的log_request实现插件式日志输出
"""
from datetime import datetime
import logging
access_log = logging.getLogger('torngas.accesslog')

class AccessLogMiddleware(object):

    def process_init(self, application):
        application.settings['log_function'] = self.log

    def log(self, handler):
        message = '%s - - [%s] "%s %s %s" %s %s "%s" "%s" %dms' % (
         handler.request.remote_ip,
         datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         handler.request.method,
         handler.request.uri,
         handler.request.version,
         handler.get_status(),
         handler.request.headers.get('Content-Length', '-'),
         handler.request.headers.get('Referer', '-'),
         handler.request.headers.get('User-Agent', '-'),
         1000.0 * handler.request.request_time())
        access_log.info(message)