# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/login/skins/easyshop.login/registered.py
# Compiled at: 2008-06-20 09:36:31
from Products.CMFCore.utils import getToolByName
utool = getToolByName(context, 'portal_url')
portal_url = utool.getPortalObject().absolute_url()
came_from = context.REQUEST.get('came_from', '')
parameters = {'came_from': came_from, '__ac_name': context.REQUEST.get('username', ''), '__ac_password': context.REQUEST.get('password', ''), 'form.submitted': '1', 'js_enabled': '1', 'cookies_enabled': '1', 'login_name': context.REQUEST.get('username', ''), 'pwd_empty': '0'}
temp = []
for (key, value) in parameters.items():
    if value != '':
        temp.append('%s=%s' % (key, value))

url = '%s/logged_in?%s' % (portal_url, ('&').join(temp))
context.REQUEST.RESPONSE.redirect(url)