# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/meta/acl.py
# Compiled at: 2013-10-23 08:11:12
"""
Created on Aug 27, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for ACL access organization.
"""
from .access import AccessMapped, EntryMapped, PropertyMapped
from .filter import FilterMapped
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint

class EntryFilterDefinition:
    """
    Provides the Entry to Filter definition.
    """
    __tablename__ = declared_attr(lambda cls: '%s_entry_filter' % cls._acl_tablename)
    __table_args__ = dict(mysql_engine='InnoDB')
    aclAccessId = declared_attr(lambda cls: Column('fk_acl_access_id', ForeignKey('%s.id' % cls._acl_tablename, ondelete='CASCADE'), primary_key=True))
    entryId = declared_attr(lambda cls: Column('fk_entry_id', ForeignKey(EntryMapped.id, ondelete='CASCADE'), primary_key=True))
    filterId = declared_attr(lambda cls: Column('fk_filter_id', ForeignKey(FilterMapped.id, ondelete='CASCADE'), primary_key=True))


class PropertyFilterDefinition:
    """
    Provides the Property to Filter definition.
    """
    __tablename__ = declared_attr(lambda cls: '%s_property_filter' % cls._acl_tablename)
    __table_args__ = dict(mysql_engine='InnoDB')
    aclAccessId = declared_attr(lambda cls: Column('fk_acl_access_id', ForeignKey('%s.id' % cls._acl_tablename, ondelete='CASCADE'), primary_key=True))
    propertyId = declared_attr(lambda cls: Column('fk_property_id', ForeignKey(PropertyMapped.id, ondelete='CASCADE'), primary_key=True))
    filterId = declared_attr(lambda cls: Column('fk_filter_id', ForeignKey(FilterMapped.id, ondelete='CASCADE'), primary_key=True))


class WithAclAccess:
    """
    Provides the ACL Access relation definition.
    """
    EntryFilter = EntryFilterDefinition
    PropertyFilter = PropertyFilterDefinition
    id = declared_attr(lambda cls: Column('id', INTEGER(unsigned=True), primary_key=True))
    accessId = declared_attr(lambda cls: Column('fk_access_id', ForeignKey(AccessMapped.Id, ondelete='CASCADE')))

    @declared_attr
    def aclId(cls):
        raise Exception('An acl id definition is required')

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint(cls.aclId, cls.accessId, name='uix_%s' % cls.__tablename__), dict(mysql_engine='InnoDB'))

    @declared_attr
    def entriesFilters(cls):
        cls.EntryFilter = type('%sEntryFilter' % cls.__name__, (cls.__bases__[0], EntryFilterDefinition), dict(_acl_tablename=cls.__tablename__))
        return relationship(cls.EntryFilter, cascade='delete')

    @declared_attr
    def propertiesFilters(cls):
        cls.PropertyFilter = type('%sPropertyFilter' % cls.__name__, (cls.__bases__[0], PropertyFilterDefinition), dict(_acl_tablename=cls.__tablename__))
        return relationship(cls.PropertyFilter, cascade='delete')