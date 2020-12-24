# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/internationalization/meta/file.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Mar 5, 2012

@package: internationalization
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for source API.
"""
from ..api.file import File
from .metadata_internationalization import meta
from ally.support.sqlalchemy.mapper import mapperModel
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Table, Column, UniqueConstraint
from sqlalchemy.types import String, DateTime
component = Column('component', String(190), nullable=True, key='Component')
plugin = Column('plugin', String(190), nullable=True, key='Plugin')
path = Column('path', String(190), nullable=False, key='Path')
table = Table('inter_file', meta, Column('id', INTEGER(unsigned=True), primary_key=True, key='Id'), component, plugin, path, Column('last_modified', DateTime, nullable=False, key='LastModified'), UniqueConstraint(component, plugin, path, name='component_plugin_path_UNIQUE'), mysql_engine='InnoDB')
File = mapperModel(File, table)