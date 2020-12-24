# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/wsgiutils_server.py
# Compiled at: 2012-02-27 07:41:53
from paste.script.serve import ensure_port_cleanup
from paste.translogger import TransLogger

def run_server(wsgi_app, global_conf, host='localhost', port=8080):
    from wsgiutils import wsgiServer
    import logging
    logged_app = TransLogger(wsgi_app)
    port = int(port)
    ensure_port_cleanup([(host, port)], maxtries=2, sleeptime=0.5)
    app_map = {'': logged_app}
    server = wsgiServer.WSGIServer((host, port), app_map)
    logged_app.logger.info('Starting HTTP server on http://%s:%s', host, port)
    server.serve_forever()