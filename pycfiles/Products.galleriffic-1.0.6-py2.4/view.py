# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/galleriffic/view.py
# Compiled at: 2011-01-18 11:08:45
from zope.interface import alsoProvides, noLongerProvides
from Products.Five import BrowserView
from Products.galleriffic.interfaces import IGallerifficView
try:
    from Products.Archetypes.interfaces._base import IBaseFolder
except:
    from Products.Archetypes.interfaces.base import IBaseFolder

from Products.ATContentTypes.interface.topic import IATTopic
interfaces_dict = {'IGallerifficView': IGallerifficView}

class CheckInterface(BrowserView):
    """ """
    __module__ = __name__

    def checkInterface(self, interface, unset=''):
        """ """

        def flagCondition():
            """
                se verifico una interfaccia di unset (unset=True), la condizione di visualizzazione della relativa azione
                e' il valore ritornato dal metodo

                se verifico una interfaccia di set, la condizione di visualizzazione della relativa azione
                e' negato rispetto al valore ritornato dal metodo
            """
            if unset:
                return False
            return True

        if not interfaces_dict.has_key(interface):
            return flagCondition()
        context = self.context
        if self.context.restrictedTraverse('@@plone').isDefaultPageInFolder():
            context = context.aq_inner.aq_parent
        if not (IBaseFolder.providedBy(context) or IATTopic.providedBy(context)):
            return flagCondition()
        iface = interfaces_dict[interface]
        return iface.providedBy(context)


class SetUnsetInterface(BrowserView):
    """ """
    __module__ = __name__

    def __call__(self):
        unset = self.request.get('unset', False)
        interface = self.request.get('iface', '')
        if not interfaces_dict.has_key(interface):
            self.context.plone_utils.addPortalMessage(interface + ' not exist')
            return self.request.response.redirect(self.context.absolute_url())
        context = self.context
        if self.context.restrictedTraverse('@@plone').isDefaultPageInFolder():
            context = context.aq_inner.aq_parent
        iface = interfaces_dict[interface]
        if unset == 'True':
            noLongerProvides(context, iface)
            context.setLayout(context.getDefaultLayout())
            self.context.plone_utils.addPortalMessage(interface + ' unset')
        else:
            alsoProvides(context, iface)
            context.setLayout('galleriffic_view')
            self.context.plone_utils.addPortalMessage(interface + ' set')
        context.reindexObject()
        return self.request.response.redirect(self.context.absolute_url())