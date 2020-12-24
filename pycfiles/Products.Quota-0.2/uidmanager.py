# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\uidmanager.py
# Compiled at: 2008-06-04 06:25:06
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from quills.remoteblogging.interfaces import IUIDManager

class UIDManager:
    """
    >>> from zope.interface.verify import verifyClass
    >>> verifyClass(IUIDManager, UIDManager)
    True
    """
    __module__ = __name__
    implements(IUIDManager)

    def __init__(self, context):
        self.context = context

    def getByUID(self, uid):
        """See IUIDManager.
        """
        if uid == '0' or uid == '' or uid is None:
            return self.context
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        lazy_cat = uid_catalog(UID=uid)
        if len(lazy_cat) > 0:
            obj = lazy_cat[0].getObject()
            return obj
        else:
            return self.context
        return

    def getUIDFor(self, obj):
        """See IUIDManager.
        """
        if obj is None:
            obj = self.context
        uid = getattr(obj, 'UID')
        if callable(uid):
            return uid()
        return uid

    def getUID(self):
        """See IUIDManager.
        """
        return self.getUIDFor(self.context)