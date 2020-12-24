# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/patient/allergies.py
# Compiled at: 2014-12-12 07:13:54
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.health import bikaMessageFactory as _
from bika.lims import bikaMessageFactory as _b
from bika.lims import PMF as _p
from bika.lims.browser import BrowserView
from bika.lims.permissions import *

class AllergiesView(BrowserView):
    template = ViewPageTemplateFile('allergies.pt')

    def __call__(self):
        if 'submitted' in self.request:
            self.context.setAllergies(self.request.form.get('Allergies', ()))
            self.context.plone_utils.addPortalMessage(_p('Changes saved'))
        return self.template()