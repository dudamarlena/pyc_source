# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/logo.py
# Compiled at: 2017-07-07 17:23:19
""" Modulo que implementa o viewlet de logo do Portal"""
from plone.app.layout.viewlets.common import LogoViewlet as ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class LogoViewlet(ViewletBase):
    """ Viewlet de redes sociais
    """
    index = ViewPageTemplateFile('templates/logo.pt')

    def portal(self):
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        portal = ps.portal()
        return portal

    def title(self):
        """ Retorna o titulo do portal
        """
        portal = self.portal()
        return getattr(portal, 'title', 'Portal Brasil')

    def title_1(self):
        """ Retorna a primeira linha do titulo do portal
        """
        portal = self.portal()
        return getattr(portal, 'title_1', 'Secretaria de')

    def title_2(self):
        """ Retorna a primeira linha do titulo do portal
        """
        portal = self.portal()
        return getattr(portal, 'title_2', 'Comunicação Social')

    def title_2_class(self):
        """ Definimos a classe a ser aplicada ao title_2
            com base no tamanho da string
        """
        title_2 = self.title_2()
        if len(title_2) > 22:
            return 'luongo'
        return 'corto'

    def orgao(self):
        """ Retorna o nome do orgao ao qual este portal
            esta vinculado
        """
        portal = self.portal()
        return getattr(portal, 'orgao', '')

    def description(self):
        """ Retorna uma breve descricao do portal
        """
        portal = self.portal()
        return getattr(portal, 'description', '')