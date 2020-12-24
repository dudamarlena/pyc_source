# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/layout/authpersonalbar/common.py
# Compiled at: 2011-04-07 04:31:16
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class PersonalBarHolderViewlet(ViewletBase):
    """Don't show the viewlet to anon users.
    """
    index = ViewPageTemplateFile('personal_bar_holder.pt')

    def update(self):
        super(PersonalBarHolderViewlet, self).update()
        self.anonymous = self.portal_state.anonymous()