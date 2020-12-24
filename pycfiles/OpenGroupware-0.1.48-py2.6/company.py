# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/company.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from base import Base, KVC
from sqlalchemy.orm import relation, backref, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

class Address(Base, KVC):
    """ An OpenGroupware Street Address Object """
    __tablename__ = 'address'
    __entityName__ = 'address'
    __internalName__ = 'Address'
    object_id = Column('address_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('company_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), nullable=False)
    version = Column('object_version', Integer)
    name1 = Column('name1', String(255))
    name2 = Column('name2', String(255))
    name3 = Column('name3', String(255))
    district = Column('district', String(255))
    street = Column('street', String(255))
    city = Column('zipcity', String(255))
    province = Column('state', String(100), quote=True)
    postal_code = Column('zip', String(50))
    country = Column('country', String(100))
    kind = Column('type', String(50), nullable=False)
    status = Column('db_status', String(50), default='inserted')

    def get_display_name(self):
        if self.street:
            return self.street
        else:
            return ('addressId#{0}').format(self.object_id)


class Telephone(Base, KVC):
    """ An OpenGroupware Telephone Object """
    __tablename__ = 'telephone'
    __entityName__ = 'telephone'
    __internalName__ = 'Telephone'
    object_id = Column('telephone_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('company_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), nullable=False)
    version = Column('object_version', Integer)
    number = Column('number', String(255))
    info = Column('info', String(255))
    kind = Column('type', String(50), nullable=False)
    status = Column('db_status', String(50))

    def __init__(self, parent_id=None, kind=None, number=None):
        self.parent_id = parent_id
        self.kind = kind
        self.number = number
        self.status = 'inserted'

    def get_display_name(self):
        if self.number:
            if self.info:
                return ('{0} [{1}]').format(self.number.strip(), self.info.strip())
            return self.number.strip()
        else:
            return ('telephoneId#{0}').format(self.object_id)

    def __repr__(self):
        return ('<Telephone objectId="{0}" parentId="{1}" kind="{2}" number="{3}"/>').format(self.object_id, self.parent_id, self.kind, self.number)


class CompanyInfo(Base, KVC):
    __tablename__ = 'company_info'
    __entityName__ = 'CompanyInfo'
    __internalName__ = 'CompanyInfo'
    object_id = Column('company_info_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('company_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), nullable=False)
    text = Column('comment', String)
    status = Column('db_status', String(50))

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        self.status = 'inserted'

    def get_display_name(self):
        return ('company assignment of objectId#{0} to objectId#{1}').format(self.object_id, self.parent_id)

    contact = relation('Contact', uselist=False, backref=backref('person', cascade='all, delete-orphan'), primaryjoin='CompanyInfo.parent_id==Contact.object_id')
    enterprise = relation('Enterprise', uselist=False, backref=backref('enterprise', cascade='all, delete-orphan'), primaryjoin='CompanyInfo.parent_id==Enterprise.object_id')


class CompanyValue(Base, KVC):
    """ An OpenGroupware CompanyValues Object """
    __tablename__ = 'company_value'
    __entityName__ = 'companyValue'
    __internalName__ = 'CompanyValue'
    object_id = Column('company_value_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('company_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), nullable=False)
    name = Column('attribute', String(255), nullable=False)
    string_value = Column('value_string', String(255))
    date_value = Column('value_date', DateTime())
    integer_value = Column('value_int', Integer)
    label = Column('label', String(255))
    uid = Column('uid', Integer)
    widget = Column('type', Integer)

    def __init__(self, parent_id, name, value=None):
        self.parent_id = parent_id
        self.name = name
        self.set_value(value)

    def set_value(self, value):
        if value is None:
            self.string_value = None
            self.integer_value = None
        elif isinstance(value, int):
            self.integer_value = value
            self.string_value = unicode(value)
        elif isinstance(value, list):
            self.integer_value = None
            self.string_value = (',').join([ unicode(x) for x in value ])
        else:
            self.string_value = unicode(value)
            if value.isdigit():
                self.integer_value = int(value)
            else:
                self.integer_value = None
        return

    def __repr__(self):
        return ('<CompanyValue objectId={0} parentId={1} name="{2}" label="{3}" stringValue="{3}">').format(self.object_id, self.parent_id, self.name, self.label, self.string_value)

    def get_display_name(self):
        return ('company attribute "{0}" of objectId#{1}').format(self.name, self.object_id)