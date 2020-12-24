# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/internationalization/meta/source.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Mar 5, 2012\n\n@package: internationalization\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the SQL alchemy meta for source API.\n'
from .metadata_internationalization import meta
from ..api.source import Source, TYPE_PYTHON, TYPE_JAVA_SCRIPT, TYPE_HTML
from .file import File
from ally.support.sqlalchemy.mapper import mapperModel
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.types import Enum
table = Table('inter_source', meta, Column('fk_file_id', ForeignKey(File.Id), primary_key=True, key='Id'), Column('type', Enum(TYPE_PYTHON, TYPE_JAVA_SCRIPT, TYPE_HTML), nullable=False, key='Type'), mysql_engine='InnoDB')
Source = mapperModel(Source, table, inherits=File)