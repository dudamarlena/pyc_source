# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/events.py
# Compiled at: 2010-05-19 10:20:52
from datetime import datetime
import logging, Globals, os.path
from AccessControl import getSecurityManager, ClassSecurityInfo
from Products.Five import BrowserView
from zope.app.component.hooks import getSite
from zope.component import getUtility
from Acquisition import aq_parent
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from collective.portlet.recentactivity.interfaces import IRecentActivityUtility

def Added(event):
    activities = getUtility(IRecentActivityUtility)
    username = getSecurityManager().getUser().getProperty('fullname')
    if not username or username == '':
        username = getSecurityManager().getUser().getId()
    activities.addActivity(DateTime(), 'added', username, event.object, aq_parent(event.object))


def Edited(event):
    activities = getUtility(IRecentActivityUtility)
    username = getSecurityManager().getUser().getProperty('fullname')
    if not username or username == '':
        username = getSecurityManager().getUser().getId()
    activities.addActivity(DateTime(), 'edited', username, event.object, aq_parent(event.object))


def Copied(event):
    """
    """
    pass


def Moved(event):
    """
    """
    pass


def Removed(event):
    """
    """
    pass