# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aws/inlineuserpref/controlpanel.py
# Compiled at: 2009-12-13 18:44:30
"""Personalisation forms"""
from zope.interface import Interface, implements
from zope.component import adapts, getAdapter, getMultiAdapter
from zope.schema import Bool
from zope.formlib import form
from Products.Five.formlib import formbase
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as p_
from aws.inlineuserpref import AWSInlineUserPrefMessageFactory as _

class IInlineEditOption(Interface):
    """Does the user prefer inline editing"""
    __module__ = __name__
    enable_inline_editing = Bool(title=_('enable_inline_editing_label', default='Enable inline editing'), description=_('enable_inline_editing_help', default='Inline Ajax editing requires a fast personal computer and a fast browser like Firefox or Safari. You may uncheck this option if you use a slow computer or use Internet Explorer 6 or 7.'), required=False)


class InlineEditOptionManager(object):
    """Our form adapter"""
    __module__ = __name__
    implements(IInlineEditOption)
    adapts(ISiteRoot)

    def __init__(self, context):
        """context is supposed to be the Plone site"""
        self.context = context
        membership_tool = getMultiAdapter((context, context.REQUEST), name='plone_tools').membership()
        self.member = membership_tool.getAuthenticatedMember()

    @apply
    def enable_inline_editing():

        def get(self):
            return self.member.getProperty('enable_inline_editing')

        def set_(self, value):
            self.member.setProperties(enable_inline_editing=bool(value))

        return property(get, set_)


class InlineEditForm(formbase.EditForm):
    """Our form
    """
    __module__ = __name__
    label = _('inline_edit_form_label', default='Inline edition preferences')
    description = _('inline_edit_form_help', default='What editing mode do you prefer.')
    form_fields = form.FormFields(IInlineEditOption)

    def __call__(self):
        self.request.set('disable_border', True)
        return super(InlineEditForm, self).__call__()

    @form.action(p_('label_save'))
    def handleApply(self, action, data):
        storage = getAdapter(self.context, IInlineEditOption)
        storage.enable_inline_editing = data['enable_inline_editing']
        IStatusMessage(self.request).addStatusMessage(p_('Changes made.'), type='info')
        self.request.RESPONSE.redirect(self.request.URL)
        return ''