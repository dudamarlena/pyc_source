# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\usermanager.py
# Compiled at: 2008-06-04 06:25:06
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from quills.remoteblogging.interfaces import IUIDManager, IUserManager
USER_INFO = {'name': 'no name', 'email': 'no email', 'userid': 'no user id', 'firstname': 'no first name', 'lastname': 'no last name', 'url': 'no url'}

class WeblogUserManager:
    """
    >>> from zope.interface.verify import verifyClass
    >>> verifyClass(IUserManager, WeblogUserManager)
    True
    """
    __module__ = __name__
    implements(IUserManager)

    def __init__(self, context):
        self.context = context

    def getWeblogsForUser(self, user_id):
        """See IUserManager.
        """
        parent_blog = self.context
        blogs = []
        blogs.append({'url': self.context.absolute_url(), 'blogid': IUIDManager(self.context).getUID(), 'blogName': self.context.Title()})
        return blogs

    def getUserInfo(self, user_id):
        """See IUserManager.
        """
        membership = getToolByName(self.context, 'portal_membership')
        info = USER_INFO.copy()
        member = membership.getAuthenticatedMember()
        if member:
            for (key, value) in info.items():
                info[key] = getattr(member, key, None) or value

        return info


class PortalUserManager:
    __module__ = __name__
    implements(IUserManager)

    def __init__(self, context):
        self.context = context

    def getWeblogsForUser(self, user_id):
        """See IUserManager.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(meta_type='Weblog', Creator=user_id)
        blogs = []
        for item in results:
            obj = item.getObject()
            blogs.append({'url': obj.absolute_url(), 'blogid': IUIDManager(obj).getUID(), 'blogName': obj.Title()})

        return blogs

    def getUserInfo(self, user_id):
        """See IUserManager.
        """
        membership = getToolByName(self.context, 'portal_membership')
        info = USER_INFO.copy()
        member = membership.getAuthenticatedMember()
        if member:
            for (key, value) in info.items():
                info[key] = getattr(member, key, None) or value

        return info