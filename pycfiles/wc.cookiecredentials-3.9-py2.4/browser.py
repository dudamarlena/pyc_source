# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/cookiecredentials/browser.py
# Compiled at: 2007-09-20 06:47:27
from zope.formlib.form import EditForm, Fields
from zope.formlib.namedtemplate import NamedTemplate
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('wc.cookiecredentials')
from zope.app.authentication.session import IBrowserFormChallenger
from wc.cookiecredentials.interfaces import ICookieCredentials

class CookieCredentialsEditForm(EditForm):
    __module__ = __name__
    form_fields = Fields(ICookieCredentials) + Fields(IBrowserFormChallenger)
    label = _('Configure cookie credentials plugin')