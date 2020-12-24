# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fapws/contrib/log.py
# Compiled at: 2009-08-20 03:05:56
import time, os.path, sys

class Log:

    def __init__(self, output=sys.stdout):
        self.output = output

    def __call__(self, f):

        def func(environ, start_response):
            res = f(environ, start_response)
            tts = time.strftime('%d/%b/%Y:%H:%M:%S', time.gmtime())
            if type(res) == type([]):
                content = ('').join(res)
                size = len(content)
            elif hasattr(res, 'name'):
                size = os.path.getsize(res.name)
            else:
                size = '-'
            remote_host = environ.get('HTTP_X_FORWARDED_FOR', environ['fapws.remote_addr'])
            self.output.write('%s %s - [%s GMT] "%s %s %s" %s %s "%s" "%s"\n' % (remote_host, environ['HTTP_HOST'], tts, environ['REQUEST_METHOD'], environ['fapws.uri'], environ['HTTP_PROTOCOL'], start_response.status_code, size, environ.get('HTTP_REFERER', '-'), environ['HTTP_USER_AGENT']))
            self.output.flush()
            return res

        return func