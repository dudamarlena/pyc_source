# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/james/.virtualenvs/thimble/lib/python2.7/site-packages/flask_prometheus/__init__.py
# Compiled at: 2017-06-09 11:21:51
import time
from prometheus_client import Counter, Histogram
from prometheus_client import start_http_server
from flask import request
latency_buckets = [ x / 20.0 for x in range(0, 20) ] + [ x / 10.0 for x in range(10, 50) ] + [ x / 5.0 for x in range(25, 50) ]
FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency', [
 'method', 'endpoint'], buckets=latency_buckets)
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count', [
 'method', 'endpoint', 'http_status'])

def before_request():
    request.start_time = time.time()
    request.reported = False


def after_request(response):
    request.reported = True
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response


def teardown_request(excn):
    if not request.reported:
        request_latency = time.time() - request.start_time
        FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
        FLASK_REQUEST_COUNT.labels(request.method, request.path, 500).inc()


def monitor(app, port=8000, addr=''):
    app.before_request(before_request)
    app.after_request(after_request)
    app.teardown_request(teardown_request)
    start_http_server(port, addr)


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    monitor(app, port=8000)

    @app.route('/')
    def index():
        return 'Hello'


    app.run()