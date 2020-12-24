# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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