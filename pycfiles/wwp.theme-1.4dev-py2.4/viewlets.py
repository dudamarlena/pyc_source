# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/theme/browser/viewlets.py
# Compiled at: 2009-07-01 06:06:54
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import PersonalBarViewlet, ViewletBase
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import datetime

class WWPLogoViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.sitehome = portal_state.navigation_root_url()


class WwpDate(ViewletBase):
    """ Custom Personal bar """
    __module__ = __name__
    index = ViewPageTemplateFile('templates/WwpDate.pt')

    def update(self):
        super(WwpDate, self).update()
        self.dateTimeNow = datetime.date.today()