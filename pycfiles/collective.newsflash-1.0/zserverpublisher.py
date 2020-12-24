# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/zserverpublisher.py
# Compiled at: 2013-12-24 05:41:42
from ZServer.PubCore.ZServerPublisher import ZServerPublisher
import newrelic.agent, newrelic.api, newrelic.api.transaction, newrelic.api.web_transaction, logging
LOG = logging.getLogger('ZServerPublisher')
original__init__ = ZServerPublisher.__init__
from collective.newrelic.utils import logger
PLACEHOLDER = 'PLACEHOLDER'

def newrelic__init__(self, accept):
    from sys import exc_info
    from ZPublisher import publish_module
    from ZPublisher.WSGIPublisher import publish_module as publish_wsgi
    trans = None
    while 1:
        try:
            (name, a, b) = accept()
            if name == 'Zope2':
                try:
                    application = newrelic.api.application.application_instance()
                    environ = {}
                    trans = newrelic.api.web_transaction.WebTransaction(application, environ)
                    trans.name_transaction(PLACEHOLDER, group='Zope2', priority=1)
                    trans.__enter__()
                    publish_module(name, request=a, response=b)
                finally:
                    b._finish()
                    if trans:
                        if trans.name == 'PLACEHOLDER':
                            newrelic.agent.ignore_transaction()
                        trans.__exit__(None, None, None)
                    a = b = None

            elif name == 'Zope2WSGI':
                try:
                    res = publish_wsgi(a, b)
                    for r in res:
                        a['wsgi.output'].write(r)

                finally:
                    a['wsgi.output']._close = 1
                    a['wsgi.output'].close()

        except:
            LOG.error('exception caught', exc_info=True)

    return


ZServerPublisher.__init__ = newrelic__init__
logger.info('Patched ZServer.PubCore.ZServerPublisher:ZServerPublisher.__init__ with WebTransaction creation, entering and exiting')