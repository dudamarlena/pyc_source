# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/commentanswer.py
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
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.Five import BrowserView
from time import time
from z3c.form import field
from zope.component import createObject
from zope.component import getUtility
from zope.interface import implementer
from zope import schema

class ICommentAnswer(form.Schema, IImageScaleTraversable):
    """
    Answer for Questions
    """
    text = schema.Text(title=_('Text'), required=True)


@implementer(ICommentAnswer)
class CommentAnswer(Container):

    def can_edit(self):
        sm = getSecurityManager()
        return sm.checkPermission('emrt.necd.content: Edit CommentAnswer', self)

    def can_add_files(self):
        sm = getSecurityManager()
        parent = aq_parent(self)
        return sm.checkPermission('emrt.necd.content: Add NECDFile', self) and api.content.get_state(parent) not in ('expert-comments', )

    def get_files(self):
        items = self.values()
        mtool = api.portal.get_tool('portal_membership')
        return [ item for item in items if mtool.checkPermission('View', item) ]

    def can_delete(self):
        sm = getSecurityManager()
        parent = aq_parent(self)
        parent_state = api.content.get_state(parent)
        return sm.checkPermission('Delete portal content', self) and parent_state not in ('expert-comments', )


class CommentAnswerView(BrowserView):

    def render(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        url = '%s#%s' % (parent.absolute_url(), context.getId())
        return self.request.response.redirect(url)


class AddForm(add.DefaultAddForm):
    label = 'Answer'
    description = ''

    def updateFields(self):
        super(AddForm, self).updateFields()
        self.fields = field.Fields(ICommentAnswer).select('text')
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


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(edit.DefaultEditForm):
    label = 'Answer'
    description = ''

    def updateFields(self):
        super(EditForm, self).updateFields()
        self.fields = field.Fields(ICommentAnswer).select('text')
        self.groups = [ g for g in self.groups if g.label == 'label_schema_default' ]

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets['text'].rows = 15

    def updateActions(self):
        super(EditForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')