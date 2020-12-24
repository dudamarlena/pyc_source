# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/browser/search.py
# Compiled at: 2008-06-25 09:25:12
from zope.interface import implements
from Products.PlonePAS.interfaces.browser import IPASSearchView
from Products.PlonePAS.browser.search import PASSearchView as PASDefaultSearchView
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from redomino.workgroup.interfaces import IWorkgroup
from redomino.workgroup.config import WORKGROUP_MEMBERDATA

class PASSearchView(PASDefaultSearchView):
    __module__ = __name__
    implements(IPASSearchView)

    def searchUsers(self, sort_by=None, **criteria):
        results = PASDefaultSearchView.searchUsers(self, sort_by, **criteria)
        if IPloneSiteRoot.providedBy(self.context):
            return results
        elif IWorkgroup.providedBy(self.context):
            filter_path = self.context.absolute_url() + '/' + WORKGROUP_MEMBERDATA
            filtered_users = filter(lambda x: filter_path in x['editurl'], results)
            portal_membership = getToolByName(self.context, 'portal_membership')
            for user_dict in filtered_users:
                user = portal_membership.getMemberById(user_dict['userid'])
                if user:
                    user_dict['user'] = user

            return filtered_users
        else:
            filter_path = WORKGROUP_MEMBERDATA
            return filter(lambda x: filter_path not in x['editurl'], results)
        return results