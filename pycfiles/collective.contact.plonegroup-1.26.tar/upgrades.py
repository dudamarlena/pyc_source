# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/upgrades/upgrades.py
# Compiled at: 2014-12-23 07:48:21
__doc__ = 'Upgrades for collective.contact.membrane.'
from ecreall.helpers.upgrade.interfaces import IUpgradeTool

def v2(context):
    """Upgrade to v2."""
    tool = IUpgradeTool(context)


def v3(context):
    """Upgrade to v3."""
    tool = IUpgradeTool(context)
    tool.runImportStep('collective.contact.membrane', 'plone.app.registry')