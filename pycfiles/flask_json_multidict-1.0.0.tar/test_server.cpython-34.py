# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/underdog/github/flask-json-multidict/flask_json_multidict/test/utils/test_server.py
# Compiled at: 2015-03-03 19:52:37
# Size of source mod 2**32: 1267 bytes
from flask import Flask, request, jsonify
from flask_json_multidict import get_json_multidict
test_server = Flask(__name__)

@test_server.route('/')
def root():
    """Endpoint to verify server is up"""
    return 'Hello World!'


@test_server.route('/echo', methods=['GET', 'POST'])
def echo():
    """Echo back `form`/`json` data"""
    body = request.form
    if request.headers['content-type'] == 'application/json':
        body = get_json_multidict(request)
    return jsonify({'method': request.method, 
     'content-type': request.headers['content-type'], 
     'body': {key:body[key] for key in body}})


@test_server.route('/list', methods=['GET', 'POST'])
def list():
    """Echo back `form`/`json` data"""
    body = request.form
    if request.headers['content-type'] == 'application/json':
        body = get_json_multidict(request)
    return jsonify({'method': request.method, 
     'content-type': request.headers['content-type'], 
     'body': {key:body.getlist(key) for key in body}})