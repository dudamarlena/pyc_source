# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/session.py
# Compiled at: 2006-09-21 05:27:39
from zope.component import adapter
from zope.app.session.http import ICookieClientIdManager
from zope.app.session.http import CookieClientIdManager
from zope.app.session.interfaces import ISessionDataContainer
from zope.app.session.session import PersistentSessionDataContainer
from worldcookery.interfaces import INewWorldCookerySiteEvent

@adapter(INewWorldCookerySiteEvent)
def setUpClientIdAndSessionDataContainer(event):
    sm = event.object.getSiteManager()
    clientids = CookieClientIdManager()
    clientids.namespace = 'worldcookery'
    clientids.cookieLifetime = 3600
    sm['clientids'] = clientids
    sm.registerUtility(sm['clientids'], ICookieClientIdManager)
    session_data = PersistentSessionDataContainer()
    session_data.timeout = 3600
    session_data.resolution = 5
    sm['session_data'] = session_data
    sm.registerUtility(sm['session_data'], ISessionDataContainer)