# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/internationalization/meta/file.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Mar 5, 2012\n\n@package: internationalization\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the SQL alchemy meta for source API.\n'
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