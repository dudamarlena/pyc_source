# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/subscribers.py
# Compiled at: 2009-03-31 04:47:33
from zope.interface import alsoProvides, noLongerProvides
from zope.component import getUtility
from interfaces import ISyndicationObject
try:
    from vice.outbound.interfaces import IFeedConfigs
    success = True
except ImportError:
    success = False

def mark_syndication(object, event):
    if hasattr(object.aq_base, 'syndication_information') or success and IFeedConfigs(object.aq_base, None) and IFeedConfigs(object.aq_base).enabled:
        if not ISyndicationObject.providedBy(object):
            alsoProvides(object, ISyndicationObject)
    elif ISyndicationObject.providedBy(object):
        noLongerProvides(object, ISyndicationObject)
    return