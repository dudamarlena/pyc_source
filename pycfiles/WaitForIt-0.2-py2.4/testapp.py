# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waitforit/testapp.py
# Compiled at: 2007-05-28 14:45:54
import time

def slow_app(environ, start_response):
    progress = environ.get('waitforit.progress', {})
    start = time.time()
    total = 10
    while time.time() - start < total:
        progress['message'] = 'Currently at %.2f seconds (started at %i)' % (time.time() - start, start)
        progress['percent'] = (time.time() - start) * 100 / total
        progress
        time.sleep(1)

    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['I was started at %i.' % start]


if __name__ == '__main__':
    from paste.httpserver import serve
    from waitforit.middleware import WaitForIt
    app = WaitForIt(slow_app, 1, 1)
    from paste.translogger import TransLogger
    app = TransLogger(app)
    serve(app, host='127.0.0.1', port='8080')