# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/zope_event.py
# Compiled at: 2013-12-24 05:41:42
from collective.newrelic.utils import logger
from zope import event
from zope.event import subscribers
import newrelic.agent

def newrelic_notify(event):
    """ Notify all subscribers of ``event``.
    """
    for subscriber in subscribers:
        nr_relic_subscriber = newrelic.agent.FunctionTraceWrapper(subscriber, event.__class__.__name__, 'Zope/Dispatch')
        nr_relic_subscriber(event)


event.notify = newrelic_notify
logger.info('Patched zope.event:notify with instrumentation')