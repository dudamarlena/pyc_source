# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to318.py
# Compiled at: 2015-11-03 03:53:39
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from bika.lims.utils import tmpID
from bika.lims.idserver import renameAfterCreation
from bika.health.permissions import AddEthnicity, ViewEthnicities
from bika.lims import logger

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup
    qi = portal.portal_quickinstaller
    ufrom = qi.upgradeInfo('bika.health')['installedVersion']
    logger.info('Upgrading Bika Health: %s -> %s' % (ufrom, '318'))
    return True