# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/Extensions/Install_inactive.py
# Compiled at: 2008-10-23 05:55:16
"""
Resources for CMF quick installer
$Id: Install_inactive.py 63643 2008-04-26 16:40:36Z clebeaupin $
"""
__author__ = ''
__docformat__ = 'restructuredtext'
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes
from iw.fss.config import PROJECTNAME, GLOBALS, fss_prefs_configlet
from iw.fss.FSSTool import FSSTool
from iw.fss.modifier import MODIFIER_ID
from iw.fss.modifier import manage_addModifier

def install_modifier(portal, out):
    """Register CMFEditions modifier
    """
    mtool = getToolByName(portal, 'portal_modifier')
    if MODIFIER_ID in mtool.objectIds():
        out.write('Modifier already installed.')
        return False
    manage_addModifier(mtool)
    out.write('Modifier installed.')
    return True


def install(self):
    out = StringIO()
    type_info = listTypes(PROJECTNAME)
    installTypes(self, out, type_info, PROJECTNAME)
    add_tool = self.manage_addProduct[PROJECTNAME].manage_addTool
    if not self.objectIds(spec=FSSTool.meta_type):
        add_tool(FSSTool.meta_type)
    install_subskin(self, out, GLOBALS)
    cp_tool = getToolByName(self, 'portal_controlpanel')
    try:
        cp_tool.registerConfiglet(**fss_prefs_configlet)
    except:
        pass

    install_modifier(self, out)
    out.write('Installation completed.\n')
    return out.getvalue()


def uninstall(self):
    out = StringIO()
    try:
        cp_tool = getToolByName(self, 'portal_controlpanel')
        cp_tool.unregisterApplication(PROJECTNAME)
    except:
        pass

    out.write('Uninstallation completed.\n')
    return out.getvalue()