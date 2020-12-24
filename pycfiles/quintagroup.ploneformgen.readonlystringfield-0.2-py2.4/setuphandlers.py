# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/ploneformgen/readonlystringfield/setuphandlers.py
# Compiled at: 2009-03-24 10:52:04
from Products.CMFCore.utils import getToolByName

def cleanUpFactoryTool(portal):
    tool = getToolByName(portal, 'portal_factory')
    if 'FormReadonlyStringField' in tool._factory_types.keys():
        del tool._factory_types['FormReadonlyStringField']


def uninstall(context):
    if context.readDataFile('quintagroup.ploneformgen.readonlystringfield_uninstall.txt') is None:
        return
    out = []
    site = context.getSite()
    cleanUpFactoryTool(site)
    return