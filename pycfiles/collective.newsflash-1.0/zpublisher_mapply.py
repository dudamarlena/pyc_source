# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/zpublisher_mapply.py
# Compiled at: 2013-12-24 05:41:42
import ZPublisher
from ZPublisher.mapply import default_missing_name, default_handle_class
import newrelic.agent, newrelic.api
from collective.newrelic.utils import logger
original_mapply = ZPublisher.mapply.mapply

def newrelic_mapply(object, positional=(), keyword={}, debug=None, maybe=None, missing_name=default_missing_name, handle_class=default_handle_class, context=None, bind=0):
    trans = newrelic.agent.current_transaction()
    with newrelic.api.function_trace.FunctionTrace(trans, name=object.__class__.__name__, group='Zope'):
        result = original_mapply(object, positional, keyword, debug, maybe, missing_name, handle_class, context, bind)
    return result


ZPublisher.mapply.mapply = newrelic_mapply
logger.info('Patched ZPublisher.mapply:mapply with instrumentation')