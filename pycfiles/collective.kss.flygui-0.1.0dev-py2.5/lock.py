# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/flygui/browser/lock.py
# Compiled at: 2008-06-16 04:30:48
from Products.Five.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize import instance
from plone.locking.interfaces import ILockable

class LockPopup(BrowserView):
    render = ViewPageTemplateFile('templates/lock_popup.pt')

    def __init__(self, context, request, uid):
        super(LockPopup, self).__init__(context, request)
        self.uid = uid

    def getLockedObject(self):
        atool = getToolByName(self.context, 'archetype_tool')
        return atool.getObject(self.uid)

    def getLockInfo(self):
        obj = self.getLockedObject()
        lockable = ILockable(obj)
        info = lockable.lock_info()
        return info[0]