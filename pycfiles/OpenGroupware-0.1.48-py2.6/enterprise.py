# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/enterprise.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from base import Base, KVC
from company import CompanyInfo
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.associationproxy import association_proxy

class Enterprise(Base, KVC):
    """ An OpenGroupware Enterprise object """
    __tablename__ = 'enterprise'
    __entityName__ = 'Enterprise'
    __internalName__ = 'Enterprise'
    object_id = Column('company_id', Integer, ForeignKey('object_acl.object_id'), ForeignKey('log.object_id'), primary_key=True)
    version = Column('object_version', Integer)
    name = Column('description', String(45))
    bank = Column('bank', String(100))
    bank_code = Column('bank_code', String(45))
    email = Column('email', String(100))
    is_enterprise = Column('is_enterprise', Integer)
    is_private = Column('is_private', Integer)
    is_read_only = Column('is_readonly', Integer)
    is_customer = Column('is_customer', Integer)
    sensitivity = Column('sensitivity', Integer)
    associated_contacts = Column('associated_contacts', String(255))
    associated_categories = Column('associated_categories', String(255))
    associated_company = Column('associated_company', String(255))
    im_address = Column('im_address', String(255))
    keywords = Column('keywords', String(255))
    URL = Column('url', String(255))
    owner_id = Column('owner_id', Integer)
    file_as = Column('fileas', String(255))
    status = Column('db_status', String(50))
    number = Column('number', String(50))
    login = Column('login', String(100))
    carddav_uid = Column('carddav_uid', String(100))
    _info = relation('CompanyInfo', uselist=False, backref=backref('company_info_enterprise'), primaryjoin='CompanyInfo.parent_id==Enterprise.object_id')

    @property
    def comment(self):
        if self._info is None:
            self._info = CompanyInfo(text='')
        return self._info.text

    @comment.setter
    def comment(self, value):
        if self._info is None:
            self._info = CompanyInfo(text=value)
        else:
            self._info.text = value
        return

    def __init__(self):
        self.is_enterprise = 1
        self.is_private = 0
        self.is_read_only = 0
        self.is_customer = 0
        self.status = 'inserted'
        self._info = CompanyInfo()

    def get_display_name(self):
        return self.name

    def get_file_name(self):
        if self.carddav_uid:
            return self.carddav_uid
        return ('{0}.vcf').format(self.object_id)