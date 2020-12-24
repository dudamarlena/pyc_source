# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/skins/upfrontcontacts/add_person.py
# Compiled at: 2010-03-10 13:47:44
__doc__ = " Create a person and set it's organisation\n"
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