# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/graphite/theme/upgrade/00090001.py
# Compiled at: 2014-10-15 08:29:12
from Acquisition import aq_inner
from Acquisition import aq_parent

def upgrade(tool):
    """ css and js names changes
    """
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup
    setup.runImportStepFromProfile('profile-graphite.theme:default', 'cssregistry')
    setup.runImportStepFromProfile('profile-graphite.theme:default', 'jsregistry')
    return True