# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upc/remotecontrol/browser/remotecontrol.py
# Compiled at: 2009-12-04 07:02:04
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Acquisition import *
from Products.GenericSetup import profile_registry, EXTENSION
from Products.CMFCore.utils import getToolByName

class ListInstancesView(BrowserView):
    __module__ = __name__

    def __call__(self):
        context = aq_inner(self.context)
        out = []
        for item in context.values():
            if IPloneSiteRoot.providedBy(item):
                out.append(item.id)

        return out


class InstallProductView(BrowserView):
    __module__ = __name__

    def __call__(self, product):
        context = aq_inner(self.context)
        success = []
        fail = []
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                result = qi.installProducts(products=[product])
                if '%s:ok' % product in result:
                    success.append(plonesite.id)
                else:
                    fail.append(plonesite.id)

        if fail:
            return 'Installing %s failed on instances (%s)' % (product, fail)
        else:
            return 'Successfully installed %s on all instances.' % product
        return


class ReinstallProductView(BrowserView):
    __module__ = __name__

    def __call__(self, product):
        context = aq_inner(self.context)
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                qi.reinstallProducts(products=[product])

        return 'Successfully reinstalled %s on all instances.' % product


class UninstallProductView(BrowserView):
    __module__ = __name__

    def __call__(self, product):
        context = aq_inner(self.context)
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                qi = getattr(plonesite, 'portal_quickinstaller', None)
                qi.uninstallProducts(products=[product])

        return 'Successfully uninstalled %s on all instances.' % product


class ApplyImportStepView(BrowserView):
    __module__ = __name__

    def __call__(self, product, step_id):
        context = aq_inner(self.context)
        for plonesite in context.values():
            if IPloneSiteRoot.providedBy(plonesite):
                setup = getattr(plonesite, 'portal_setup', None)
                profile_id = 'profile-%s:default' % product
                setup.runImportStepFromProfile(profile_id, step_id, run_dependencies=True, purge_old=None)

        return 'Successfully applied import step %s to profile %s.' % (step_id, product)