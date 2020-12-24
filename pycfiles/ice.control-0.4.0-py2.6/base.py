# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/details/base/base.py
# Compiled at: 2010-08-27 06:32:04
from zope.dublincore.interfaces import IZopeDublinCore
from zope.app.component.browser.registration import IRegistrationDisplay
from zope.component import getSiteManager, getMultiAdapter

def _registrations(context, comp):
    sm = getSiteManager(context)
    for r in sm.registeredUtilities():
        if r.component == comp or comp is None:
            yield r

    for r in sm.registeredAdapters():
        if r.factory == comp or comp is None:
            yield r

    for r in sm.registeredSubscriptionAdapters():
        if r.factory == comp or comp is None:
            yield r

    for r in sm.registeredHandlers():
        if r.factory == comp or comp is None:
            yield r

    return


class DetailsInfoBase:

    def getTitle(self):
        dc = IZopeDublinCore(self.context, None)
        return dc and dc.title

    def getRegistrations(self):
        return [ getMultiAdapter((r, self.request), IRegistrationDisplay) for r in sorted(_registrations(self.context, self.context))
               ]