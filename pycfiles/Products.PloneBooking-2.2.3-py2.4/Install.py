# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\Extensions\Install.py
# Compiled at: 2008-11-19 15:29:05
"""
    PloneBooking: Installation script
"""
__version__ = '$Revision: 1.16 $'
__author__ = ''
__docformat__ = 'restructuredtext'
from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.PloneBooking import BookingPermissions
from Products.PloneBooking.BookingTool import BookingTool
from Products.PloneBooking.config import GLOBALS, PROJECTNAME, SKINS_DIR
from Products.PloneBooking.BookingPermissions import *
from StringIO import StringIO
plonebooking_workflows = (
 (
  'folder_workflow', ('BookingCenter', ), False, False), ('booking_workflow', ('Booking', ), True, False), ('bookable_object_workflow', ('BookableObject', ), True, False))

def addWorkflow(self, out):
    workflowTool = getToolByName(self, 'portal_workflow')
    for (name, types, create, default) in plonebooking_workflows:
        if create and name not in workflowTool.objectIds():
            installFunc = ExternalMethod('temp', 'temp', PROJECTNAME + '.' + name, 'create' + name.capitalize())
            workflow = installFunc(name)
            workflowTool._setObject(name, workflow)
        if types:
            workflowTool.setChainForPortalTypes(types, name)
        if default:
            workflowTool.setDefaultChain(name)

    out.write('Workflow added')


def DEPRECATED_install(self):
    out = StringIO()
    typeInfo = listTypes(PROJECTNAME)
    installTypes(self, out, typeInfo, PROJECTNAME)
    add_tool = self.manage_addProduct[PROJECTNAME].manage_addTool
    if not self.objectIds(spec=BookingTool.meta_type):
        add_tool(BookingTool.meta_type)
    install_subskin(self, out, GLOBALS)
    self.manage_permission(BookingPermissions.AddBooking, ('Member', 'Owner', 'Manager'), 1)
    pftool = getToolByName(self, 'portal_factory')
    pftool.manage_setPortalFactoryTypes(listOfTypeIds=('Booking', 'BookableObject'))
    addActionIcon(self, category='plone', action_id='book', icon_expr='booking.gif', title='Book an object', priority=0)
    ntp = getToolByName(self, 'portal_properties').navtree_properties
    bl = list(ntp.getProperty('metaTypesNotToList', ()))
    if 'Booking' not in bl:
        bl.append('Booking')
        ntp._p_changed = 1
        ntp.metaTypesNotToList = bl
    out.write('Installation completed.\n')
    return out.getvalue()


def addActionIcon(self, category, action_id, icon_expr, title=None, priority=0):
    ai = getToolByName(self, 'portal_actionicons')
    if ai.queryActionInfo(category, action_id):
        ai.updateActionIcon(category, action_id, icon_expr, title, priority)
    else:
        ai.addActionIcon(category, action_id, icon_expr, title, priority)


def DEPRECATED_uninstall(self):
    out = StringIO()
    wf_tool = getToolByName(self, 'portal_workflow')
    for (workflow_id, types, create, default) in plonebooking_workflows:
        if create and workflow_id in wf_tool.objectIds():
            wf_tool._delObject(workflow_id)

    out.write('Workflow uninstalled.\n')
    out.write('Uninstallation completed.\n')
    return out.getvalue()