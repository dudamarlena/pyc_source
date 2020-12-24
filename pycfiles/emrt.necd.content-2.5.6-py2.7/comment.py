# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/comment.py
# Compiled at: 2019-02-15 13:51:23
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition.interfaces import IAcquirer
from emrt.necd.content import MessageFactory as _
from plone import api
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.Five import BrowserView
from time import time
from z3c.form import field
from zope import schema
from zope.component import createObject
from zope.component import getUtility
from zope.interface import implementer

class IComment(form.Schema, IImageScaleTraversable):
    """
    Q&A item
    """
    text = schema.Text(title=_('Text'), required=True)


@implementer(IComment)
class Comment(Container):

    def can_edit(self):
        sm = getSecurityManager()
        return sm.checkPermission('emrt.necd.content: Edit Comment', self)

    def can_delete(self):
        sm = getSecurityManager()
        return sm.checkPermission('Delete portal content', self)

    def can_add_files(self):
        sm = getSecurityManager()
        return sm.checkPermission('emrt.necd.content: Add NECDFile', self)

    def get_files(self):
        items = self.values()
        mtool = api.portal.get_tool('portal_membership')
        return [ item for item in items if mtool.checkPermission('View', item) ]


class CommentView(BrowserView):

    def render(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        url = '%s#%s' % (parent.absolute_url(), context.getId())
        return self.request.response.redirect(url)


class AddForm(add.DefaultAddForm):
    label = 'Question'
    description = ''

    def updateFields(self):
        super(AddForm, self).updateFields()
        self.fields = field.Fields(IComment).select('text')
        self.groups = [ g for g in self.groups if g.label == 'label_schema_default' ]

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def create(self, data={}):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        content = createObject(fti.factory)
        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())
        if IAcquirer.providedBy(content):
            content = content.__of__(container)
        id = str(int(time()))
        content.title = id
        content.id = id
        content.text = self.request.form.get('form.widgets.text', '')
        return aq_base(content)

    def updateActions(self):
        super(AddForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(edit.DefaultEditForm):
    label = 'Question'
    description = ''

    def updateFields(self):
        super(EditForm, self).updateFields()
        self.fields = field.Fields(IComment).select('text')
        self.groups = [ g for g in self.groups if g.label == 'label_schema_default' ]

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def updateActions(self):
        super(EditForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')


def add_question(context, event):
    """ When adding a question, go directly to
        'open' status on the observation
    """
    question = aq_parent(context)
    observation = aq_parent(question)
    with api.env.adopt_roles(roles=['Manager']):
        if api.content.get_state(obj=question) == 'closed' and api.content.get_state(obj=observation) == 'close-requested':
            api.content.transition(obj=observation, transition='reopen')
            api.content.transition(obj=question, transition='reopen')
        if api.content.get_state(observation) == 'draft':
            api.content.transition(obj=observation, transition='open')