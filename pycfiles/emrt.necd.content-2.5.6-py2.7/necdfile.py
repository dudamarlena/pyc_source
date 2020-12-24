# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/necdfile.py
# Compiled at: 2019-02-15 13:51:23
from AccessControl import getSecurityManager
from Acquisition import aq_parent
from emrt.necd.content import MessageFactory as _
from plone.dexterity.browser import add
from plone.dexterity.content import Item
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from zope import schema
from zope.interface import implementer

class INECDFile(form.Schema, IImageScaleTraversable):
    """
    Files with special needs
    """
    title = schema.TextLine(title=_('Title'), required=False)
    form.primary('file')
    file = NamedBlobFile(title=_('File'), required=True)


@implementer(INECDFile)
class NECDFile(Item):

    def can_edit(self):
        sm = getSecurityManager()
        parent = aq_parent(self)
        edit = False
        if parent.portal_type == 'Comment':
            edit = sm.checkPermission('emrt.necd.content: Edit Comment', self)
        elif parent.portal_type == 'CommentAnswer':
            edit = sm.checkPermission('emrt.necd.content: Edit CommentAnswer', self)
        return edit


class AddForm(add.DefaultAddForm):
    label = 'file'
    description = ''

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        super(AddForm, self).handleAdd(self, action)
        question = self.context.aq_parent
        self.request.response.redirect(question.absolute_url())

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        super(AddForm, self).handleCancel(action)

    def update(self):
        super(AddForm, self).update()
        status = IStatusMessage(self.request)
        msg = _('Handling of confidential files: Please zip your file, protect it with a password, upload it to your reply in the EEA review tool and send the password per email to the EMRT-NECD Secretariat mailbox. Your password will only be shared with the lead reviewer and sector Expert. ')
        status.add(msg, type='info')

    def updateFields(self):
        super(AddForm, self).updateFields()
        self.fields = field.Fields(INECDFile).omit('title')
        self.groups = [ g for g in self.groups if g.label == 'label_schema_default' ]


class AddView(add.DefaultAddView):
    form = AddForm


class NECDFileView(BrowserView):

    def render(self):
        url = aq_parent(self.context).absolute_url()
        return self.response.redirect(url)