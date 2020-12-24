# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wymypy/libs/flask.py
# Compiled at: 2013-12-02 14:53:17
from werkzeug.serving import WSGIRequestHandler

class WyMyPyRequestHandler(WSGIRequestHandler):
    wbufsize = -1


def join_result(func):

    def call_and_join(*args, **kwargs):
        result = func(*args, **kwargs)
        return ('').join(result)