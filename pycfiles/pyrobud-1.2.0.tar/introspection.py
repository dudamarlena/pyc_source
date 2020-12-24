# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/introspection.py
# Compiled at: 2015-01-26 11:58:05
import logging
logger = logging.getLogger('robots.introspection')
import threading
introspection = None
if False:
    try:
        import Pyro4, Pyro4.errors
        uri = 'PYRONAME:robots.introspection'
        try:
            introspection = Pyro4.Proxy(uri)
            introspection.initiate(str(0))
            logger.info('Connection to the introspection server established.')
        except Pyro4.errors.CommunicationError:
            logger.warning('Introspection server not running. No introspection.')
            introspection = None
        except Pyro4.errors.NamingError:
            logger.warning('Introspection server not running (no name server). No introspection.')
            introspection = None

    except ImportError:
        pass