# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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