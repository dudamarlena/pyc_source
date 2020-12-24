# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/skins/upfrontcontacts/add_person.py
# Compiled at: 2010-03-10 13:47:44
""" Create a person and set it's organisation
"""
from Products.CMFCore.utils import getToolByName
person_id = context.generateUniqueId('Person')
session = None
sdm = getToolByName(context, 'session_data_manager', None)
if sdm is not None:
    session = sdm.getSessionData(create=0)
    if session is None:
        session = sdm.getSessionData(create=1)
session.set(person_id, {'Organisation': organisation_uid})
person = context.restrictedTraverse('portal_factory/Person/' + person_id)
context.REQUEST.RESPONSE.redirect('%s/edit' % person.absolute_url())