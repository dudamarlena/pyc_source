# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/utils.py
# Compiled at: 2007-10-06 08:08:40
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting.config import ENCODING

def getMemberInfo(context, member_id, name, email):
    """
    """
    mtool = getToolByName(context, 'portal_membership')
    if member_id is not None:
        member_id = member_id.encode('utf-8')
    member = mtool.getMemberById(member_id)
    if name != '':
        name = name
    elif member_id != '':
        mi = mtool.getMemberInfo(member_id)
        name = mi and mi['fullname'] or member_id
    else:
        name = 'Anonymous'
    if email != '':
        email = email
    elif member_id != '':
        email = member and member.getProperty('email', '') or ''
    else:
        email = ''
    return {'name': name, 'email': email, 'is_manager': member and member.has_role('Manager')}