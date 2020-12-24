# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/support/meta/configuration.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on May 22, 2013

@package: livedesk
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Martin Saturka

Contains the SQL alchemy meta for configurations API.
"""
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.ext.declarative import declared_attr

def abstractMapping():
    raise Exception('Use a derived class')


class ConfigurationDescription:
    """
    Provides abstract mapping for Configuration.
    """
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Name = declared_attr(lambda cls: Column('name', String(255), primary_key=True))
    Value = declared_attr(lambda cls: Column('value', String(1024)))
    parent = declared_attr(lambda cls: abstractMapping())