# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/PortalContent.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl
from AccessControl import SecurityManagement
from AccessControl.Permissions import view, view_management_screens, access_contents_information
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.DynamicType import DynamicType
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
from Products.CMFCore.utils import getToolByName

class PortalContent(DynamicType, DefaultDublinCoreImpl, PropertyManager, SimpleItem, CMFCatalogAware):
    """
    Sort out our default views ...
    """
    isPortalContent = 1
    _isPortalContent = 1
    __factory_meta_type__ = None
    __ac_permissions__ = DefaultDublinCoreImpl.__ac_permissions__ + PropertyManager.__ac_permissions__ + ((view, ('status', 'actions', 'getTypeInfo')), (access_contents_information, ('getStatusOf', 'getActionsFor', 'instigator'))) + SimpleItem.__ac_permissions__ + CMFCatalogAware.__ac_permissions__
    manage_options = PropertyManager.manage_options + ({'label': 'View', 'action': ''},) + SimpleItem.manage_options

    def _getPortalTypeName(self):
        """
        needed for the portal type view mechanism ...
        """
        return self.meta_type

    def status(self):
        """
        return workflow status
        """
        try:
            return getToolByName(self, 'portal_workflow').getInfoFor(self, 'review_state')
        except:
            return ''

    def _status(self, status, wftool=None, wf=None, wf_var='review_state'):
        """
        set workflow status without calling workflow transition (use content_modify_status
        method if you want to do this ...
        """
        wftool = wftool or getToolByName(self, 'portal_workflow')
        wf = wf or wftool.getWorkflowsFor(self)[0]
        assert status in wf.states.objectIds(), 'unknown state: %s (not in %s)' % (status, wf.states.objectIds())
        wftool.setStatusOf(wf.getId(), self, {'review_state': status})

    def actions(self):
        """
        return  a list of valid transitions for the object
        """
        return getToolByName(self, 'portal_actions').listFilteredActionsFor(self)['workflow']

    def getStatusOf(self, workflow):
        """
        return the status of ourselves in the context of this workflow (the corresponding
        WorkflowTool function is strangely declared private ...
        """
        try:
            return getToolByName(self, 'portal_workflow').getInfoFor(self, workflow.state_var)
        except WorkflowException:
            return 'Doh'

    def getActionsFor(self, workflow):
        """
        return a list of valid transition states
        """
        state = workflow._getWorkflowStateOf(self)
        return state.getTransitions()

    def instigator(self):
        """
        return who owns (ie enacted) the content
        """
        try:
            return self.getOwnerTuple()[1]
        except:
            return ''

    def indexObject(self):
        """"""
        self.catalog_object(self, ('/').join(self.getPhysicalPath()))

    def unindexObject(self):
        """"""
        self.uncatalog_object(('/').join(self.getPhysicalPath()))

    def reindexObject(self, idxs=[]):
        """"""
        self.unindexObject()
        self.indexObject()

    def manage_afterAdd(self, item, container):
        """"""
        self.indexObject()

    def manage_beforeDelete(self, item, container):
        """"""
        self.unindexObject()

    def SecurityCheckPermission(md, permission, object):
        """Check whether the security context allows the given permission on
        the given object.

        Arguments:
        
        permission -- A permission name
        
        object -- The object being accessed according to the permission
        """
        return SecurityManagement.getSecurityManager().checkPermission(permission, object)


AccessControl.class_init.InitializeClass(PortalContent)