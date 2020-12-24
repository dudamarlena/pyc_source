# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/sc/base/hotsites/subscribers.py
# Compiled at: 2009-12-29 13:58:42
from zope.component import getMultiAdapter, getUtility
from sc.base.hotsites.interfaces import IHotSite, INoHotSite
from sc.base.hotsites import MessageFactory as _
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from plone.portlets.interfaces import IPortletManager, ILocalPortletAssignmentManager
from plone.portlets.constants import CONTENT_TYPE_CATEGORY, CONTEXT_CATEGORY, GROUP_CATEGORY
from Acquisition import aq_inner, aq_parent
from Products.statusmessages.interfaces import IStatusMessage
K_PREFIX = 'sc.hotsite'

def newHotSite(obj):
    folder = obj.object
    if IHotSite.providedBy(folder):
        props = getToolByName(folder, 'portal_properties')
        confs = props.hotsites_conf
        allowedCTs = confs.allowedContentTypes
        skin_name = confs.skin_name
        default_view_id = confs.default_view_id
        default_view_path = confs.default_view_path
        workflow_id = confs.workflow_id
        use_accessibility = confs.use_accessibility
        value = getBlockedPortlets(folder, 'plone.rightcolumn')
        save_value(folder, 'plone.rightcolumn', value)
        value = getBlockedPortlets(folder, 'plone.leftcolumn')
        save_value(folder, 'plone.leftcolumn', value)
        portlet_blacklist = folder.restrictedTraverse('set-portlet-blacklist-status')
        portlet_blacklist(manager='plone.rightcolumn', group_status=1, content_type_status=1, context_status=1)
        portlet_blacklist(manager='plone.leftcolumn', group_status=1, content_type_status=1, context_status=1)
        save_value(folder, 'constrainTypesMode', folder.getConstrainTypesMode())
        save_value(folder, 'locallyAllowedTypes', folder.getLocallyAllowedTypes())
        save_value(folder, 'immediatelyAddableTypes', folder.getImmediatelyAddableTypes())
        folder.setConstrainTypesMode(1)
        folder.setLocallyAllowedTypes(allowedCTs)
        folder.setImmediatelyAddableTypes(allowedCTs)
        script_body = "\ncontext.changeSkin('%s', context.REQUEST)\nreturn 1\n        " % skin_name
        if 'setSkin' not in folder.objectIds():
            folder.manage_addProduct['PythonScripts'].manage_addPythonScript('setSkin')
        folder['setSkin'].write(script_body)
        folder.manage_addProduct['SiteAccess'].manage_addAccessRule('setSkin')
        change_default_view = False
        if default_view_id not in folder.objectIds():
            if default_view_path:
                obj_tmpl = folder.unrestrictedTraverse(default_view_path, None)
                if obj_tmpl:
                    container = aq_parent(aq_inner(obj_tmpl))
                    obj = container.manage_copyObjects([obj_tmpl.getId()])
                    results = folder.manage_pasteObjects(obj)
                    nw_obj = [ r for r in results if r['id'] == obj_tmpl.getId() ]
                    nw_obj = nw_obj[0]
                    nw_obj_id = nw_obj['new_id']
                    folder.manage_renameObjects([nw_obj_id], [default_view_id])
                    nw_obj = folder[default_view_id]
                    wt = getToolByName(folder, 'portal_workflow')
                    if 'publish' in [ w['id'] for w in wt.getTransitionsFor(nw_obj) ]:
                        wt.doActionFor(nw_obj, 'publish')
                    nw_obj.reindexObject()
                    change_default_view = True
                else:
                    msg = _('Default view template ${path} not found.', mapping={'path': default_view_path})
                    IStatusMessage(folder.request).addStatusMessage(msg, type='info')
        else:
            change_default_view = True
        if use_accessibility and 'accessibility' not in folder.objectIds():
            folder.invokeFactory('Document', id='accessibility')
        save_value(folder, 'layout', folder.getLayout())
        if change_default_view:
            folder.setLayout(default_view_id)
        if WorkflowPolicyConfig_id not in folder.objectIds():
            folder.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
            config = getattr(folder, WorkflowPolicyConfig_id)
        else:
            config = getToolByName(folder, 'portal_placeful_workflow').getWorkflowPolicyConfig(folder)
        config.setPolicyBelow(workflow_id)
        getToolByName(folder, 'portal_workflow').updateRoleMappings()
    elif INoHotSite.providedBy(folder):
        portlet_blacklist = folder.restrictedTraverse('set-portlet-blacklist-status')
        (c_content, c_context, c_group) = get_value(folder, 'plone.rightcolumn')
        portlet_blacklist(manager='plone.rightcolumn', group_status=c_group, content_type_status=c_content, context_status=c_content)
        (c_content, c_context, c_group) = get_value(folder, 'plone.leftcolumn')
        portlet_blacklist(manager='plone.leftcolumn', group_status=c_group, content_type_status=c_content, context_status=c_content)
        visao_padrao = get_value(folder, 'layout')
        if visao_padrao is not None:
            folder.setLayout(visao_padrao)
        constrainTypesMode = get_value(folder, 'constrainTypesMode')
        if constrainTypesMode is not None:
            folder.setConstrainTypesMode(constrainTypesMode)
        locallyAllowedTypes = get_value(folder, 'locallyAllowedTypes')
        if locallyAllowedTypes is not None:
            folder.setLocallyAllowedTypes(locallyAllowedTypes)
        immediatelyAddableTypes = get_value(folder, 'immediatelyAddableTypes')
        if immediatelyAddableTypes is not None:
            folder.setImmediatelyAddableTypes(immediatelyAddableTypes)
        folder.manage_addProduct['SiteAccess'].manage_addAccessRule(None)
        if 'setSkin' in folder.objectIds():
            pass
        if WorkflowPolicyConfig_id in folder.objectIds():
            config = getToolByName(folder, 'portal_placeful_workflow').getWorkflowPolicyConfig(folder)
            config.setPolicyBelow('default_policy')
            getToolByName(folder, 'portal_workflow').updateRoleMappings()
    return


def save_value(obj, key, value):
    """ save the value in the obj, with the key using Annotation,
    using a prefix to the key
    """
    ann_obj = IAnnotations(obj)
    ann_obj['%s.%s' % (K_PREFIX, key)] = value


def get_value(obj, key):
    """ Returns the value from obj, using the Annoation with a key prefix
    """
    ann_obj = IAnnotations(obj)
    return ann_obj.get('%s.%s' % (K_PREFIX, key), None)


def getBlockedPortlets(context, manager_name):
    """ Returns the blocked configuration of portlets in the context
    returns a tuple (CONTENT_TYPE_CATEGORY, CONTEXT_CATEGORY, GROUP_CATEGORY) """
    manager = getUtility(IPortletManager, manager_name)
    assignable = getMultiAdapter((context, manager), ILocalPortletAssignmentManager)
    c_content = assignable.getBlacklistStatus(CONTENT_TYPE_CATEGORY)
    c_context = assignable.getBlacklistStatus(CONTEXT_CATEGORY)
    c_group = assignable.getBlacklistStatus(GROUP_CATEGORY)
    return (
     c_content, c_context, c_group)