# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve2044.py
# Compiled at: 2019-02-15 13:51:23
from logging import getLogger
from plone import api
LOGGER = getLogger(__name__)

def run(_):
    upgrade_reviewfolders()


def upgrade_reviewfolders():
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='ReviewFolder')
    for brain in brains:
        brain.getObject().type = 'inventory'