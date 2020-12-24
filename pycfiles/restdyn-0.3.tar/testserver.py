# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/namlook/Documents/projects/restdyn/tests/testserver.py
# Compiled at: 2011-09-02 10:32:08
from bottle import route, run, request
import json

@route('/tests/jsonquery')
def index():
    return json.dumps(json.loads(request.GET.get('q')))


run(host='localhost', port=8080)