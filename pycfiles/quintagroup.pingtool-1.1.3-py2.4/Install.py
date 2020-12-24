# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/Extensions/Install.py
# Compiled at: 2009-03-31 04:47:31
from zope.component import getSiteManager
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
ADAPTERNAMES = ('pingtool_extender', 'canonical_url_adapter', '')

def uninstall_componentRegistryAdapter(self, ADAPTERNAME):
    sm = getSiteManager(self)
    registrations = tuple(sm.registeredAdapters())
    for registration in registrations:
        if registration.name == ADAPTERNAME:
            factory = registration.factory
            required = registration.required
            provided = registration.provided
            name = registration.name
            sm.unregisterAdapter(factory=factory, required=required, provided=provided, name=name)


def uninstall(self):
    out = StringIO()
    for ADAPTERNAME in ADAPTERNAMES:
        uninstall_componentRegistryAdapter(self, ADAPTERNAME)
        print >> out, '\nSuccessfully uninstalled %s adapter.' % ADAPTERNAME

    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-quintagroup.pingtool:uninstall')
    print >> out, 'Imported uninstall profile.'
    return out.getvalue()