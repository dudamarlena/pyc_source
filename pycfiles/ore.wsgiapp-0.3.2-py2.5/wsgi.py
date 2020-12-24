# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/wsgiapp/wsgi.py
# Compiled at: 2008-05-01 10:27:18
"""A WSGI Application wrapper for zope

"""
import logging
from zope.event import notify
from zope import component
from zope.interface import implements
from zope.publisher.publish import publish
from zope.app.appsetup import appsetup
from zope.app.publication.httpfactory import HTTPPublicationRequestFactory
from zope.app.wsgi import interfaces
from interfaces import IApplication, WSGIApplicationCreatedEvent

class WSGIPublisherApplication(object):
    """A WSGI application implementation for the zope publisher

    Instances of this class can be used as a WSGI application object.

    The class relies on a properly initialized request factory.
    """
    implements(interfaces.IWSGIApplication)

    def __init__(self, db=None, factory=HTTPPublicationRequestFactory):
        self.requestFactory = factory(db)

    def __call__(self, environ, start_response):
        """See zope.app.wsgi.interfaces.IWSGIApplication"""
        request = self.requestFactory(environ['wsgi.input'], environ)
        handle_errors = environ.get('wsgi.handleErrors', True)
        request = publish(request, handle_errors=handle_errors)
        response = request.response
        start_response(response.getStatusString(), response.getHeaders())
        return response.consumeBodyIter()


class PMDBWSGIPublisherApplication(WSGIPublisherApplication):

    def __call__(self, environ, start_response):
        environ['wsgi.handleErrors'] = False
        try:
            app = super(PMDBWSGIPublisherApplication, self)
            return app.__call__(environ, start_response)
        except Exception, error:
            import sys, pdb
            print '%s:' % sys.exc_info()[0]
            print sys.exc_info()[1]
            try:
                pdb.post_mortem(sys.exc_info()[2])
                raise
            finally:
                pass


def config(zcml_conf, devmode, features=()):
    if devmode:
        features += ('devmode', )
        logging.warning('Developer mode is enabled: this is a security risk and should NOT be enabled on production servers. Developer mode can be turned off in etc/zope.conf')
    appsetup.config(zcml_conf, features=features)
    app = component.getUtility(IApplication)
    notify(WSGIApplicationCreatedEvent(app))
    return


def getWSGIApplication(configfile, schemafile=None, features=(), requestFactory=HTTPPublicationRequestFactory):
    config(configfile, schemafile, features)
    return WSGIPublisherApplication(None, requestFactory)