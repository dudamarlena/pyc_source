# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/services.py
# Compiled at: 2018-10-18 17:35:13
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter

class ServicesViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/services.pt')

    def update(self):
        super(ServicesViewlet, self).update()
        context = aq_inner(self.context)
        portal_services_view = getMultiAdapter((context, self.request), name='plone_context_state')
        self.portal_services = portal_services_view.actions('portal_services')