# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/browser/signupform.py
# Compiled at: 2006-09-21 05:27:34
from zope.formlib.form import AddForm, EditForm, Fields
from zope.formlib.namedtemplate import NamedTemplate
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery')
from zope.app.authentication.principalfolder import IInternalPrincipalContainer
from worldcookery.signup import ISignup, SignupPrincipalFolder

class SignupAddForm(AddForm):
    __module__ = __name__
    form_fields = Fields(IInternalPrincipalContainer) + Fields(ISignup)
    label = _('Add signup principal folder')
    template = NamedTemplate('worldcookery.form')

    def create(self, data):
        folder = SignupPrincipalFolder(data['prefix'])
        folder.signup_roles = data['signup_roles']
        return folder


class SignupEditForm(EditForm):
    __module__ = __name__
    form_fields = Fields(ISignup)
    label = _('Configure signup principal folder')
    template = NamedTemplate('worldcookery.form')