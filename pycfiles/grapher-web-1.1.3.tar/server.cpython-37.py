# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vpaslav/projects/grapher-web/grapher/web/server.py
# Compiled at: 2020-01-13 08:56:14
# Size of source mod 2**32: 444 bytes
import os, http.server
from functools import partial
from grapher import web
PORT = 4200
HOSTNAME = ''
Handler = partial((http.server.SimpleHTTPRequestHandler),
  directory=(os.path.join)(*web.__path__, *('ui', )))
with http.server.HTTPServer((HOSTNAME, PORT), Handler) as (httpd):
    print('Warning! This is not production server. Use it only for local testing.')
    print('Listening on http://0.0.0.0:4200')
    httpd.serve_forever()