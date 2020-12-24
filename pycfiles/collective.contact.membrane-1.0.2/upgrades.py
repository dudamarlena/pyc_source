# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/upgrades/upgrades.py
# Compiled at: 2014-12-23 07:48:21
"""Upgrades for collective.contact.membrane."""
from ecreall.helpers.upgrade.interfaces import IUpgradeTool

def v2(context):
    """Upgrade to v2."""
    tool = IUpgradeTool(context)


def v3(context):
    """Upgrade to v3."""
    tool = IUpgradeTool(context)
    tool.runImportStep('collective.contact.membrane', 'plone.app.registry')