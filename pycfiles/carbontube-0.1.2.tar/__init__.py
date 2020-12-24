# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabrielfalcao/projects/personal/carbontube/carbontube/web/__init__.py
# Compiled at: 2017-07-22 19:23:27
from __future__ import unicode_literals
import uuid, json, logging, coloredlogs, gevent.pool
from gevent import pywsgi
from plant import Node
from flask import Flask, render_template, Response
from carbontube.storage import RedisStorageBackend
node = Node(__file__)
server = Flask(__name__, static_folder=node.dir.join(b'dist'), template_folder=node.dir.join(b'templates'))

def json_response(data, code=200, headers={}):
    serialized = json.dumps(data, indent=2)
    headers[b'Content-Type'] = b'application/json'
    return Response(serialized, status=code, headers=headers)


@server.route(b'/')
def index():
    return render_template(b'index.html')


@server.route(b'/api/pipelines')
def api_pipelines():
    data = server.backend.list_pipelines()
    print b'pipelines', data
    return json_response(data)


@server.route(b'/api/queues')
def api_queues():
    data = server.backend.list_job_types()
    print b'queues', data
    return json_response(data)


@server.route(b'/api/workers/available')
def api_workers_available():
    data = sorted(map(dict, server.backend.list_all_available_workers()), key=lambda w: w[b'checkin'])
    return json_response(data)


@server.route(b'/api/jobs')
def api_jobs_by_type():
    payload = server.backend.retrieve_jobs()
    return json_response(payload)


def run_server(host, port, pipeline_name, redis_uri, level=logging.INFO, debug=True, secret_key=None, concurrency=10):
    coloredlogs.install(level=level)
    server.debug = debug
    server.backend = RedisStorageBackend(pipeline_name, redis_uri=redis_uri)
    server.backend.connect()
    server.config[b'SECRET_KEY'] = secret_key or bytes(uuid.uuid4())
    pool = gevent.pool.Pool(concurrency)
    green_server = pywsgi.WSGIServer((
     host, port), server, spawn=pool)
    green_server.serve_forever()