# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web2py_utils/email_sms/db.py
# Compiled at: 2010-05-09 22:17:01
from gluon.sql import Field
from carriers import CARRIERS
fields = {'name': Field('name', notnull=True, unique=True), 
   'gateway': Field('gateway', notnull=True), 
   'email': Field('email', requires=IS_NULL_OR(IS_EMAIL())), 
   'phone': Field('phone', requires=IS_NULL_OR(IS_LENGTH(10, 10))), 
   'carrier': Field('carrier', 'reference carrier')}

def make_carriers(db, tablename='carrier'):
    return db.define_table(tablename, fields['name'], fields['gateway'])


def populate_carriers(db, tablename='carrier'):
    if db(db[tablename].id > 0).count == 0:
        for c in CARRIERS:
            db[tablename].insert(name=c['fields']['name'], gateway=c['fields']['gateway'])

        return True
    else:
        return False


def SMSVirtual(tablename, phone_field='phone', carrier_field='carrier'):

    class _SMSVirtual:

        def sms(self):
            if self[tablename].get(carrier_field):
                return self[tablename][field].gateway % dict(phone_number=self[tablename][phone_field])
            else:
                return
                return