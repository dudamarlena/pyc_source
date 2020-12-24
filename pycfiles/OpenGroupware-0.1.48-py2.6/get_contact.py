# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/get_contact.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import *
from coils.logic.address import GetCompany
from command import ContactCommand

class GetContact(GetCompany, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        self.access_check = True
        GetCompany.__init__(self)
        self._carddav_uid = None
        self._email = None
        return

    def parse_parameters(self, **params):
        GetCompany.parse_parameters(self, **params)
        if 'uid' in params:
            self._carddav_uid = unicode(params.get('uid'))
            self.set_single_result_mode()
        if 'email' in params:
            self._email = params.get('email').lower()
            self.set_multiple_result_mode()
        self._archived = params.get('archived', False)
        if 'properties' in params:
            self._properties = params.get('properties')
        else:
            self._properties = [
             Contact]

    def run(self):
        db = self._ctx.db_session()
        if self._carddav_uid is not None:
            query = db.query(*self._properties).filter(and_(Contact.status != 'archived', Contact.carddav_uid == self._carddav_uid))
        elif self._email is not None:
            if self._archived:
                query = db.query(*self._properties).join(CompanyValue).filter(and_(CompanyValue.string_value.ilike(self._email), CompanyValue.name.in_(['email1', 'email2', 'email3'])))
            else:
                query = db.query(*self._properties).join(CompanyValue).filter(and_(CompanyValue.string_value.ilike(self._email), CompanyValue.name.in_(['email1', 'email2', 'email3']), Contact.status != 'archived'))
        elif self._archived:
            query = db.query(*self._properties).filter(and_(Contact.object_id.in_(self.object_ids), Contact.is_person == 1))
        else:
            query = db.query(*self._properties).filter(and_(Contact.object_id.in_(self.object_ids), Contact.is_person == 1, Contact.status != 'archived'))
        x = query.all()
        self.set_return_value(x)
        return