# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/person.py
# Compiled at: 2010-08-08 03:18:44
"""Person model"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from pysvnmanager.model.meta import Session, Base
from pysvnmanager.model.ldap_api import LDAP
import logging
log = logging.getLogger(__name__)

class Person(Base):
    __tablename__ = 'person'
    uid = Column(String(100), primary_key=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    nickname = Column(String(100))
    mail = Column(String(100))

    def __init__(self, uid='', firstname='', lastname='', nickname='', mail=''):
        if not isinstance(firstname, unicode):
            firstname = unicode(firstname, 'utf-8')
        if not isinstance(lastname, unicode):
            lastname = unicode(lastname, 'utf-8')
        if not isinstance(nickname, unicode):
            nickname = unicode(nickname, 'utf-8')
        if not isinstance(mail, unicode):
            mail = unicode(mail, 'utf-8')
        if not isinstance(uid, unicode):
            uid = unicode(uid, 'utf-8')
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.mail = mail

    def __repr__(self):
        return "<Person('%s, %s')" % (self.uid, self.nickname)


def sync_users_with_ldap(config):
    result = []
    ldap = LDAP(config)
    if not ldap.is_bind():
        return False
    lusers = {}
    for (dn, ldap_dict) in ldap.fetch_all_users():
        if ldap.verbose:
            log.debug('Find user: %r' % dn)
        uid = ldap_dict.get(ldap.attr_uid)[0]
        lusers[uid] = {'dn': dn, 
           'name': uid, 
           'firstname': unicode(ldap_dict.get(ldap.attr_givenname, [''])[0], 'utf-8'), 
           'lastname': unicode(ldap_dict.get(ldap.attr_sn, [''])[0], 'utf-8'), 
           'nickname': unicode(ldap_dict.get(ldap.attr_cn, [''])[0], 'utf-8'), 
           'mail': unicode(ldap_dict.get(ldap.attr_mail, [''])[0], 'utf-8')}

    dbusers = {}
    for person in Session.query(Person).all():
        dbusers[person.uid] = person

    lset = set(lusers.keys())
    dbset = set(dbusers.keys())
    count = 0
    for uid in lset - dbset:
        count += 1
        log.debug('add user: %r' % uid)
        person = Person(uid=uid, firstname=lusers[uid]['firstname'], lastname=lusers[uid]['lastname'], nickname=lusers[uid]['nickname'], mail=lusers[uid]['mail'])
        Session.add(person)

    if count:
        Session.commit()
    result.append(count)
    count = 0
    for uid in dbset - lset:
        count += 1
        log.debug('Delete user: %r' % uid)
        Session.delete(dbusers[uid])

    if count:
        Session.commit()
    result.append(count)
    count = 0
    for uid in dbset & lset:
        if dbusers[uid].firstname != lusers[uid]['firstname'] or dbusers[uid].lastname != lusers[uid]['lastname'] or dbusers[uid].mail != lusers[uid]['mail'] or dbusers[uid].nickname != lusers[uid]['nickname']:
            count += 1
            log.debug('Update user: %r' % uid)
            Session.delete(dbusers[uid])
            person = Person(uid=uid, firstname=lusers[uid]['firstname'], lastname=lusers[uid]['lastname'], nickname=lusers[uid]['nickname'], mail=lusers[uid]['mail'])
            Session.add(person)

    if count:
        Session.commit()
    result.append(count)
    return result