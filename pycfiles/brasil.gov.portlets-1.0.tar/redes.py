# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/browser/viewlets/redes.py
# Compiled at: 2017-11-02 19:53:49
__doc__ = ' Modulo que implementa o viewlet de redes sociais do Portal'
from brasil.gov.portal.config import REDES
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class RedesSociaisViewlet(ViewletBase):
    """ Viewlet de redes sociais
    """
    index = ViewPageTemplateFile('templates/redessociais.pt')
    redes = []

    def update(self):
        """ Prepara/Atualiza os valores utilizados pelo Viewlet
        """
        super(RedesSociaisViewlet, self).update()
        tools = self.context.restrictedTraverse('@@plone_tools')
        pp = tools.properties()
        configs = getattr(pp, 'brasil_gov', None)
        redes = {}
        for rede in REDES:
            redes[rede['id']] = rede

        if configs:
            data = configs.getProperty('social_networks', [])
            selected = []
            for item in data:
                k, v = item.split('|')
                rede_info = redes[k]
                selected.append({'site': k, 'title': rede_info['title'], 
                   'info': v, 
                   'url': rede_info['url'] % v})

            self.redes = selected
        return

    def available(self):
        return self.redes and True or False