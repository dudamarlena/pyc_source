# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/browser/options_tab.py
# Compiled at: 2007-10-07 06:50:12
from zope.app.form.browser import MultiSelectWidget
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.CMFCore.utils import getToolByName
from Products.Five.formlib import formbase
from Products.Five.browser import pagetemplatefile
from iqpp.plone.commenting.config import *
from iqpp.plone.commenting.interfaces import ICommentingOptions

class MyMultiSelectWidget(MultiSelectWidget):
    __module__ = __name__

    def __init__(self, field, request):
        """
        """
        super(MyMultiSelectWidget, self).__init__(field, field.value_type.vocabulary, request)


class CommentingOptionsTab(formbase.EditForm):
    """
    """
    __module__ = __name__
    form_fields = form.FormFields(ICommentingOptions)
    form_fields['edit_own_comments'].custom_widget = MyMultiSelectWidget
    template = pagetemplatefile.ZopeTwoPageTemplateFile('options_tab.pt')

    @form.action('add')
    def action_add(self, action, data):
        """
        """
        ro = ICommentingOptions(self.context)
        for field in self.form_fields:
            name = field.__name__
            if name in data.keys():
                setattr(ro, name, data[name])

        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(MESSAGES['options-saved'])
        url = self.context.absolute_url() + '/commenting-options'
        self.request.response.redirect(url)