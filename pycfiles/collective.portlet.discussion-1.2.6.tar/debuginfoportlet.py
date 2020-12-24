# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/portlet/debuginfo/debuginfoportlet.py
# Compiled at: 2009-02-05 06:53:22
from zope.interface import implements, Attribute
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent, aq_base
from collective.portlet.debuginfo import DebugInfoPortletMessageFactory as _
DEFAULT_PERMISSIONS = ('Access contents information', 'Add portal content', 'Modify portal content',
                       'Review portal content', 'View')
DEFAULT_ATTRIBUTES = ('CreationDate', )

class IDebugInfoPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    show_info = schema.Bool(title=_('User Info'), description=_("Check to display current user's info."), default=True, required=False)
    show_roles = schema.Bool(title=_('User Roles'), description=_("Check to display current user's roles in the current context."), default=True, required=False)
    watched_attrs = schema.Tuple(title=_('Watched attributes'), description='Define possible attributes or methods which you want to watch for the current context.', default=DEFAULT_ATTRIBUTES, required=False, value_type=schema.ASCIILine(title=_('Name')))
    show_permissions = schema.Bool(title=_('User Permissions'), description=_("Check to display current user's permissions (defined below) in the current context."), default=True, required=False)
    selected_permissions = schema.Tuple(title=_('Selected Permissions'), description=_('Select permission(s) to display its assignment for the current user.'), default=DEFAULT_PERMISSIONS, required=False, value_type=schema.Choice(vocabulary='collective.portlet.debuginfo.vocabularies.Permissions'))


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IDebugInfoPortlet)

    def __init__(self, show_info=True, show_roles=True, watched_attrs=DEFAULT_ATTRIBUTES, show_permissions=True, selected_permissions=DEFAULT_PERMISSIONS):
        self.show_info = show_info
        self.show_roles = show_roles
        self.watched_attrs = watched_attrs
        self.show_permissions = show_permissions
        self.selected_permissions = selected_permissions

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'Debug Info Portlet'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('debuginfoportlet.pt')

    def user_info(self):
        if not self.data.show_info:
            return
        user = self._current_user()
        return dict(username=user.getId(), fullname=user.fullname or 'N/A', email=user.email or 'N/A', home_page=user.home_page or 'N/A')

    def user_roles(self):
        if not self.data.show_roles:
            return
        roles = self._current_user().getRolesInContext(self.context)
        roles.sort()
        return (', ').join(roles)

    def user_permissions(self):
        if not self.data.show_permissions:
            return
        result = {}
        user = self._current_user()
        for perm in self.data.selected_permissions:
            result[perm] = user.has_permission(perm, self.context)

        return result

    def watch(self):
        if not self.data.watched_attrs:
            return
        result = {}
        for item in self.data.watched_attrs:
            attr = self.context.get(item, None)
            if (attr is not None) & callable(attr):
                attr = attr()
            result[item] = attr or 'N/A'

        return result

    def _current_user(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getAuthenticatedMember()


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IDebugInfoPortlet)
    form_fields['selected_permissions'].custom_widget = MultiCheckBoxVocabularyWidget
    label = _('Add Debug Info Portlet')
    description = _('This portlet lists some usefull debugging info about current user in the current context.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IDebugInfoPortlet)
    form_fields['selected_permissions'].custom_widget = MultiCheckBoxVocabularyWidget
    label = _('Add Debug Info Portlet')
    description = _('This portlet lists some usefull debugging info about current user in the current context.')