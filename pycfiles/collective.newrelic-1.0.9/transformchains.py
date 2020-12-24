# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/transformchains.py
# Compiled at: 2013-12-24 05:41:42
from plone.transformchain.transformer import ConflictError, getAdapters, ITransform, LOGGER, sort_key, Transformer, DISABLE_TRANSFORM_REQUEST_KEY
from ZServer.FTPRequest import FTPRequest
import newrelic.agent
from collective.newrelic.utils import logger
original_transform_call = Transformer.__call__

def newrelic_transform__call__(self, request, result, encoding):
    if isinstance(request, FTPRequest):
        return
    else:
        if request.environ.get(DISABLE_TRANSFORM_REQUEST_KEY, False):
            return
        try:
            published = request.get('PUBLISHED', None)
            handlers = [ v[1] for v in getAdapters((published, request), ITransform) ]
            handlers.sort(sort_key)
            trans = newrelic.agent.current_transaction()
            for handler in handlers:
                with newrelic.agent.FunctionTrace(trans, handler.__class__.__name__, 'Zope/Transform'):
                    if isinstance(result, unicode):
                        newResult = handler.transformUnicode(result, encoding)
                    elif isinstance(result, str):
                        newResult = handler.transformBytes(result, encoding)
                    else:
                        newResult = handler.transformIterable(result, encoding)
                    if newResult is not None:
                        result = newResult

            return result
        except ConflictError:
            raise
        except Exception, e:
            LOGGER.exception('Unexpected error whilst trying to apply transform chain')

        return


Transformer.__call__ = newrelic_transform__call__
logger.info('Patched plone.transformchain.transformer:Transformer.__call__ with instrumentation')