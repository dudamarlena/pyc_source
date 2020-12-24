# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benoitc/work/gunicorn/src/grainbows/examples/test_keepalive.py
# Compiled at: 2010-03-16 11:27:21
from wsgiref.validate import validator

def app(environ, start_response):
    """Application which cooperatively pauses 10 seconds before responding"""
    data = 'Hello, World!\n'
    status = '200 OK'
    response_headers = [
     ('Content-type', 'text/plain'),
     (
      'Content-Length', str(len(data)))]
    start_response(status, response_headers)
    return iter([data])