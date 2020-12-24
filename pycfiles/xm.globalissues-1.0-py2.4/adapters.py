# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/xm/globalissues/adapters.py
# Compiled at: 2009-02-19 10:13:15
from zope import component

class GlobalIssueGetter(object):
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_tools = component.getMultiAdapter((context, request), name='plone_tools')
        self.catalog = self.portal_tools.catalog()

    def get_issues(self, **kwargs):
        """Get a list of issue brains.

        This implementation will get all issues in the instance which are 
        in-progress or unconfirmed

        """
        query = dict(portal_type='PoiIssue', review_state=['in-progress', 'open', 'unconfirmed', 'new'], path='/')
        query.update(kwargs)
        return self.catalog(**query)