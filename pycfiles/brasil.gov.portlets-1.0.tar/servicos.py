# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/servicos.py
# Compiled at: 2018-06-11 09:46:52
__doc__ = ' Modulo que implementa o viewlet de servicos do Portal'
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ServicosViewlet(ViewletBase):
    """ Viewlet de listagem de servicos
    """
    index = ViewPageTemplateFile('templates/servicos.pt')

    def update(self):
        """ Prepara/Atualiza os valores utilizados pelo Viewlet
        """
        super(ServicosViewlet, self).update()
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        tools = self.context.restrictedTraverse('@@plone_tools')
        portal = ps.portal()
        self._folder = 'servicos' in portal.objectIds() and portal['servicos']
        self._ct = tools.catalog()

    def available(self):
        return self._folder and True or False

    def servicos(self):
        ct = self._ct
        folder_path = ('/').join(self._folder.getPhysicalPath())
        portal_types = ['Link']
        results = ct.searchResults(portal_type=portal_types, path=folder_path, sort_on='getObjPositionInParent')
        return results