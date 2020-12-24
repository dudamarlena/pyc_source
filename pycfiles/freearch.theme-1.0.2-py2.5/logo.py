# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/browser/logo.py
# Compiled at: 2008-06-18 05:21:29
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class LogoViewlet(ViewletBase):
    """ Render site logo. 
    
    Override viewlet to use our custom template. 
    """
    render = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()
        self.navigation_root_url = self.portal_state.navigation_root_url()