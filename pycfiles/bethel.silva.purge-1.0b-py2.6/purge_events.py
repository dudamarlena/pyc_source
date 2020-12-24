# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/silva/purge/tests/grok/purge_events.py
# Compiled at: 2012-05-22 15:36:42
from five import grok
from zope.component import getUtility
from z3c.caching.interfaces import IPurgeEvent
from silva.core.interfaces import IVersion
from bethel.silva.purge.interfaces import IPurgingService

@grok.subscribe(IPurgeEvent)
def simple_purge(event):
    context = event.object
    service = getUtility(IPurgingService, context=context)
    if not hasattr(service.aq_explicit, 'test_counter'):
        service.test_counter = []
    service.test_counter.append(event.object)