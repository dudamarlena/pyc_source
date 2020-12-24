# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/user.py
# Compiled at: 2008-06-20 09:35:17
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase
from easyshop.core.config import _
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import IShop

class IUserAddForm(Interface):
    """
    """
    __module__ = __name__
    username = schema.TextLine(title=_('Username'), description=_('Username'), default='', required=False)
    password_1 = schema.TextLine(title=_('Password'), description=_('Please enter your password.'), default='', required=False)
    password_2 = schema.TextLine(title=_('Password Confirmation'), description=_('Please confirm your password.'), default='', required=False)


class ShopUserAddForm:
    """
    """
    __module__ = __name__
    implements(IUserAddForm)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    username = ''
    password_1 = ''
    password_2 = ''


class UserAddForm(formbase.AddForm):
    """
    """
    __module__ = __name__
    template = pagetemplatefile.ZopeTwoPageTemplateFile('user.pt')
    form_fields = form.Fields(IUserAddForm)
    label = _('Add User')
    form_name = _('Add User')

    @form.action(_('label_save', default='Save'), condition=form.haveInputWidgets, name='save')
    def handle_save_action(self, action, data):
        """
        """
        self.createAndAdd(data)

    def createAndAdd(self, data):
        """
        """
        username = data.get('username')
        username = username.encode('utf-8')
        password = data.get('password_1')
        request = self.context.REQUEST
        rtool = getToolByName(self.context, 'portal_registration')
        rtool.addMember(username, password)
        utool = getToolByName(self.context, 'portal_url')
        portal_url = utool.getPortalObject().absolute_url()
        came_from = ICheckoutManagement(self.context).getNextURL('AFTER_ADDED_USER')
        parameters = {'came_from': came_from, '__ac_name': username, '__ac_password': password, 'form.submitted': '1', 'js_enabled': '1', 'cookies_enabled': '1', 'login_name': username, 'pwd_empty': '0'}
        temp = []
        for (key, value) in parameters.items():
            if value != '':
                temp.append('%s=%s' % (key, value))

        url = '%s/logged_in?%s' % (portal_url, ('&').join(temp))
        request.RESPONSE.redirect(url)