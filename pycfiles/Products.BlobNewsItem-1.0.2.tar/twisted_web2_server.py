# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/twisted_web2_server.py
# Compiled at: 2012-02-27 07:41:53


def run_twisted(wsgi_app, global_conf, host='127.0.0.1', port='8080'):
    host = host or None
    import twisted.web2.wsgi, twisted.web2.log, twisted.web2.channel, twisted.web2.server, twisted.internet.reactor
    wsgi_resource = twisted.web2.wsgi.WSGIResource(wsgi_app)
    resource = twisted.web2.log.LogWrapperResource(wsgi_resource)
    twisted.web2.log.DefaultCommonAccessLoggingObserver().start()
    site = twisted.web2.server.Site(resource)
    factory = twisted.web2.channel.HTTPFactory(site)
    twisted.internet.reactor.listenTCP(int(port), factory, interface=host)
    twisted.internet.reactor.run()
    return