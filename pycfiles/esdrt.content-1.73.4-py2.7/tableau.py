# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/browser/tableau.py
# Compiled at: 2020-04-08 10:59:15
from zExceptions import Unauthorized
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import plone.api as api

class DashboardView(BrowserView):
    index = ViewPageTemplateFile('./templates/tableau_dashboard.pt')

    def __call__(self):
        if self.can_access(self.context):
            return self.index(tableau_embed=self.context.tableau_statistics)
        raise Unauthorized('Cannot access dashboard.', self.context)

    @staticmethod
    def can_access(context):
        has_embed = context.tableau_statistics
        can_access = context.tableau_statistics_roles
        if has_embed and can_access:
            user = api.user.get_current()
            roles = api.user.get_roles(user=user, obj=context)
            return set(roles).intersection(can_access)