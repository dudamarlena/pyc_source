# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/tracker/content/issue.py
# Compiled at: 2011-09-23 03:41:19
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from AccessControl.interfaces import IRoleManager
from plone.app.discussion.browser.comments import CommentsViewlet
from Products.CMFPlone.utils import log
from ageliaco.tracker import _
import datetime
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from DateTime import DateTime
from plone.indexer import indexer

class TwiceSameSupevisor(Invalid):
    """_"""


class GroupMembers(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    grok.implements(IContextSourceBinder)

    def __init__(self, group_name):
        self.group_name = group_name

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        group = acl_users.getGroupById(self.group_name)
        terms = []
        terms.append(SimpleVocabulary.createTerm('', str(''), ''))
        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

        return SimpleVocabulary(terms)


class getUserWithRole(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    grok.implements(IContextSourceBinder)

    def __init__(self, role_name):
        self.role_name = role_name

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        parent = context.aq_inner.aq_parent
        log('context : ' + context.__name__ + ' parent : ' + parent.__name__)
        users_roles = context.get_local_roles()
        users_with_the_role = [ x[0] for x in users_roles if self.role_name in x[1] ]
        while parent.Type() == 'Tracker':
            parent_users_roles = parent.get_local_roles()
            parent_users_with_the_role = [ x[0] for x in parent_users_roles if self.role_name in x[1] ]
            users_with_the_role += parent_users_with_the_role
            parent = parent.aq_parent

        terms = []
        terms.append(SimpleVocabulary.createTerm('', str(''), ''))
        if users_with_the_role is not None:
            for member_id in users_with_the_role:
                log(member_id)
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

        return SimpleVocabulary(terms)


class IIssue(form.Schema):
    """
    Issue
    """
    responsible = schema.Choice(title=_('Responsable'), description=_('Personne qui supervise cette tâche'), source=getUserWithRole('Reviewer'), required=False)
    content = RichText(title=_('Présentation'), description=_('Description de la tâche'), required=True)
    deadline = schema.Datetime(title=_('Deadline'), required=False)


class AddForm(dexterity.AddForm):
    grok.name('issue')


@form.default_value(field=IIssue['deadline'])
def startDefaultValue(data):
    year = datetime.timedelta(days=365)
    return datetime.datetime.today() + year


@grok.subscribe(IIssue, IObjectAddedEvent)
def setReviewer(issue, event):
    log('=== Default Reviewer Role Attribution in Issue ===')
    acl_users = getToolByName(issue, 'acl_users')
    mail_host = getToolByName(issue, 'MailHost')
    portal_url = getToolByName(issue, 'portal_url')
    parent = issue.aq_inner.aq_parent
    log(parent.__name__ + 'parent local roles : ' + str(parent.get_local_roles()) + "\naq_parent'parent local roles : " + str(parent.aq_parent.get_local_roles()))
    users_with_the_role = []
    if parent.Type() == 'Tracker':
        log("Testing parent's reviewers")
        users_roles = parent.get_local_roles()
        log('users roles : ' + str(users_roles))
        users_with_the_role = [ x[0] for x in users_roles if 'Reviewer' in x[1] ]
        for member in users_with_the_role:
            log('member : ' + member)

    if IRoleManager.providedBy(issue):
        for member in users_with_the_role:
            log('adding roles (Reviewer) to ' + member)
            issue.manage_addLocalRoles(member, ['Reviewer'])


@indexer(IIssue)
def deadlineIndexer(obj):
    return DateTime(obj.deadline.isoformat())


grok.global_adapter(deadlineIndexer, name='deadline')