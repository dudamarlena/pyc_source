# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/controlpanel/commenting.py
# Compiled at: 2007-10-07 08:25:12
from zope.app.form.browser import MultiSelectWidget
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.formlib import form
from zope import schema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm
from iqpp.plone.commenting.config import *

class IPloneCommentingControlPanel(Interface):
    """
    """
    __module__ = __name__
    is_enabled = schema.Bool(title=_('Is enabled'), description=_('Are comments enabled?'), default=True)
    is_moderated = schema.Bool(title=_('Is moderated'), description=_('Are comments moderated?'), required=True, default=True)
    show_preview = schema.Bool(title=_('Show Preview'), description=_('Must comments be previewed prior to adding?'), default=False)
    edit_own_comments = schema.List(title=_('Owner can edit comments'), description=_('User is allowed to edit own comment, when it is in one of selected states.'), required=False, value_type=schema.Choice(__name__='edit_own_comments', title='Review State', default='pending', vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(REVIEW_STATES_CHOICES[1:])))
    send_comment_added_mail = schema.Bool(title=_('Send email notifications?'), description=_('Should an email be sent for every new comment?'), default=False)
    mail_from = schema.TextLine(title=_('Email sender address'), description=_("The email address that will be used as sender for mails notifying about a new comment. Leave it blank to use Plone's global email address."), default=_(''), required=False)
    mail_to = schema.TextLine(title=_('Email recipient address'), description=_("The address to which notifications about new comments should be sent. Leave it blank to use Plone's global email address."), default=_(''), required=False)


class MyMultiSelectWidget(MultiSelectWidget):
    __module__ = __name__

    def __init__(self, field, request):
        """
        """
        super(MyMultiSelectWidget, self).__init__(field, field.value_type.vocabulary, request)


class PloneCommentingControlPanelForm(ControlPanelForm):
    """
    """
    __module__ = __name__
    form_fields = form.Fields(IPloneCommentingControlPanel)
    form_fields['edit_own_comments'].custom_widget = MyMultiSelectWidget
    label = _('Commenting settings')
    description = _('Here you can set global commenting options.')
    form_name = _('Commenting settings')


class PloneCommentingControlPanelAdapter(SchemaAdapterBase):
    """
    """
    __module__ = __name__
    implements(IPloneCommentingControlPanel)
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        """
        """
        super(PloneCommentingControlPanelAdapter, self).__init__(context)

    edit_own_comments = ProxyFieldProperty(IPloneCommentingControlPanel['edit_own_comments'])
    is_enabled = ProxyFieldProperty(IPloneCommentingControlPanel['is_enabled'])
    is_moderated = ProxyFieldProperty(IPloneCommentingControlPanel['is_moderated'])
    show_preview = ProxyFieldProperty(IPloneCommentingControlPanel['show_preview'])
    send_comment_added_mail = ProxyFieldProperty(IPloneCommentingControlPanel['send_comment_added_mail'])
    mail_to = ProxyFieldProperty(IPloneCommentingControlPanel['mail_to'])
    mail_from = ProxyFieldProperty(IPloneCommentingControlPanel['mail_from'])