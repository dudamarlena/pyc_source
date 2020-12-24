# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/setuphandlers.py
# Compiled at: 2009-03-31 04:47:33
from Products.CMFCore.utils import getToolByName
from quintagroup.pingtool.config import SITES_LIST, PROJECTNAME

def setupVarious(context):
    if context.readDataFile('%s_various.txt' % PROJECTNAME) is None:
        return
    portal = context.getSite()
    existent_sites = portal.portal_pingtool.objectIds()
    for site in SITES_LIST:
        if site[0] not in existent_sites:
            portal.portal_pingtool.invokeFactory(id=site[0], type_name='PingInfo', title=site[1], url=site[2])

    return


def removeConfiglet(self):
    if self.readDataFile('%s-uninstall.txt' % PROJECTNAME) is None:
        return
    portal_conf = getToolByName(self.getSite(), 'portal_controlpanel')
    portal_conf.unregisterConfiglet('portal_pingtool')
    return