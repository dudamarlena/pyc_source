# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/memberreplace/browser/controlpanel.py
# Compiled at: 2009-03-07 19:02:29
"""
MemberReplace control panel
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import transaction
from zope.interface import Interface, implements
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.schema import TextLine
from zope.schema import Bool
from zope.formlib import form
from zope.app.form.interfaces import WidgetInputError
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from iw.memberreplace.utils import IwMemberReplaceMessageFactory as _
from iw.memberreplace.utils import logger
from iw.memberreplace.config import SUBTRANSACTION_THRESHOLD

class IMemberReplaceSchema(Interface):
    __module__ = __name__
    former_member = TextLine(title=_('label_former_member', default='Former member id'), description=_('help_former_member', default='User id of the member to be replaced.'), required=True)
    new_member = TextLine(title=_('label_new_owner', default='New member id'), description=_('help_new_owner', default='User id of the member who will replace former member.'), required=True)
    change_ownership = Bool(title=_('label_change_ownership', default='Replace in ownership'), description=_('help_change_ownership', default='Replace in Zope owners of content items.'))
    change_creator = Bool(title=_('label_change_creator', default='Replace in creators'), description=_('help_change_creator', default='Replace in DC creators of content items.'))
    change_sharings = Bool(title=_('label_change_sharings', default='Replace in sharings'), description=_('help_change_sharings', default='Grant the same privileges in sharings.'))
    change_groups = Bool(title=_('label_change_groups', default='Replace in groups'), description=_('help_change_groups', default="Replace in mutable groups. This doesn't work for groups provided by LDAP or a RDBMS."))
    delete_former_member = Bool(title=_('label_delete_former_member', default='Delete former member?'), description=_('help_delete_former_member', default='Delete former member after operation if its source is mutable?'))
    dry_run = Bool(title=_('label_dry_run', default='Dry run'), description=_('help_dry_run', default='Just for testing if this can be achieved.'))
    log_process = Bool(title=_('label_log_process', default='Log changes'), description=_('help_log_process', default="Writes details of the replacement process in the event log. Watch lines prefixed with 'iw.memberreplace'."))


class MemberReplaceControlPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IMemberReplaceSchema)

    def __init__(self, context):
        """Minimal adapter"""
        self.former_member = ''
        self.new_member = ''
        self.change_ownership = False
        self.change_creator = False
        self.change_sharings = False
        self.change_groups = False
        self.delete_former_member = False
        self.dry_run = False
        self.log_process = False


class MemberReplaceControlPanel(ControlPanelForm):
    """Our control panel handler"""
    __module__ = __name__
    form_fields = form.FormFields(IMemberReplaceSchema)
    label = _('title_changing_member', default='Changing member')
    description = _('description_changing_member', default='Replacing an user by another across the site (might take some minutes on large sites)')
    form_name = _('title_changing_member', default='Changing member')

    def validate(self, action, data):
        ret = super(MemberReplaceControlPanel, self).validate(action, data)
        error_fields = [ x.field_name for x in ret ]
        errors = []
        for user_field in ('former_member', 'new_member'):
            if user_field in error_fields:
                continue
            if not self._exists_user(data[user_field]):
                title_widget = self.widgets[user_field]
                error = WidgetInputError(field_name=user_field, widget_title=title_widget.label, errors=_('error_no_such_user', default='No such user'))
                title_widget._error = error
                errors.append(error)

        if len(errors) == 0 and data['former_member'] == data['new_member']:
            for user_field in ('former_member', 'new_member'):
                title_widget = self.widgets[user_field]
                error = WidgetInputError(field_name=user_field, widget_title=title_widget.label, errors=_('error_duplicate_user', default='User ids must be different'))
                title_widget._error = error
                errors.append(error)

        if len(errors) == 0 and data['delete_former_member']:
            portal_membership = getMultiAdapter((self.context, self.request), name='plone_tools').membership()
            member = portal_membership.getMemberById(data['former_member'])
            if not member.canDelete():
                error = WidgetInputError(field_name='delete_former_member', widget_title=self.widgets['delete_former_member'].label, errors=_('error_cannot_delete_member', default='Member cannot be deleted. Probably in a non mutable source.'))
                self.widgets['delete_former_member']._error = error
                errors.append(error)
        one_checked = reduce(lambda x, y: x or y, [ data[k] for k in data.keys() if k.startswith('change_') ])
        if not one_checked:
            title_widget = self.widgets['change_ownership']
            error = WidgetInputError(field_name='change_ownership', widget_title=title_widget.label, errors=_('error_at_least_one_change', default='You must select one or more change checkbox'))
            title_widget._error = error
            errors.append(error)
        return ret + errors

    def _exists_user(self, user_id):
        plone_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        uf = plone_state.portal().acl_users
        return uf.getUserById(str(user_id)) is not None

    def _on_save(self, data=None):
        self._mustlog = data['log_process']
        really_run = not data['dry_run']
        former_member = str(data['former_member'])
        new_member = str(data['new_member'])
        plone_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        uf = plone_state.portal().acl_users
        uf_path = ('/').join(uf.getPhysicalPath())[1:]
        new_user_ob = uf.getUserById(new_member)
        plone_tools = getMultiAdapter((self.context, self.request), name='plone_tools')
        types_tool = plone_tools.types()
        valid_types = types_tool.listContentTypes()
        catalog = plone_tools.catalog()
        changes_count = 0
        for brain in catalog():
            changed = False
            brain_url = brain.getURL()
            if brain.portal_type not in valid_types:
                continue
            item = brain.getObject()
            if item is None:
                self.log('Ghost object at %s, you should refresh the catalog', brain_url)
                continue
            if data['change_ownership']:
                pass
            else:
                item_oi = item.owner_info()
                if item_oi['explicit']:
                    if item_oi['id'] == former_member and item_oi['path'] == uf_path:
                        if really_run:
                            changed = True
                            item.changeOwnership(new_user_ob)
                        self.log('Changed ownership of %s', brain_url)
                if data['change_creator']:
                    creators = item.Creators()
                    if former_member in creators:
                        creators = list(creators)
                        i = creators.index(former_member)
                        creators[i] = new_member
                        if really_run:
                            changed = True
                            item.setCreators(creators)
                        self.log('Changed creators in %s', brain_url)
                if data['change_sharings']:
                    local_roles = item.get_local_roles_for_userid(former_member)
                    if local_roles:
                        new_member_lr = item.get_local_roles_for_userid(new_member)
                        new_member_lr = list(set(new_member_lr) | set(local_roles))
                        if really_run:
                            changed = True
                            item.manage_delLocalRoles([former_member])
                            item.manage_addLocalRoles(new_member, new_member_lr)
                        self.log('Changed sharings in %s', brain_url)
                if changed:
                    changes_count += 1
                    catalog.reindexObject(item, idxs=['allowedRolesAndUsers', 'Creator'])
                if changes_count > 0 and changes_count % SUBTRANSACTION_THRESHOLD == 0:
                    transaction.savepoint(optimistic=True)
                    self.log('Committing subtransaction after %s items changed', changes_count)

        if data['change_groups']:
            former_user_ob = uf.getUserById(former_member)
            portal_groups = getToolByName(self.context, 'portal_groups')
            for group_id in former_user_ob.getGroupIds():
                group = uf.getGroupById(group_id)
                if not group.canAddToGroup(group_id):
                    self.log("Can't replace user in group %s, not mutable group", group_id)
                    continue
                if really_run:
                    portal_groups.removePrincipalFromGroup(former_member, group_id)
                    portal_groups.addPrincipalToGroup(new_member, group_id)
                self.log('Replaces %s with %s in group %s', former_member, new_member, group_id)

        if data['delete_former_member']:
            if really_run:
                portal_membership = plone_tools.membership()
                portal_membership.deleteMembers([data['former_member']], delete_memberareas=0, delete_localroles=1)
            self.log('Removed member %s', data['former_member'])
        self.log('Properties/ownership changed in %s object', changes_count)
        if not really_run:
            self.log('Dry run mode, aborting changes')
        return

    def log(self, text, *args):
        if self._mustlog:
            logger.info(text, *args)