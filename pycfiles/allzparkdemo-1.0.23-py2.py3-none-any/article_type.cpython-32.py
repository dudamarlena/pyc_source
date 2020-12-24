# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/support/sqlalchemy/samples/meta/article_type.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Aug 25, 2011\n\n@package: ally core sql alchemy\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the SQL alchemy meta for article type API.\n'
from . import meta
from ..api.article_type import ArticleType
from ally.support.sqlalchemy.mapper import mapperModel
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import String, Integer
table = Table('article_type', meta, Column('id', Integer, primary_key=True, key='Id'), Column('name', String(255), nullable=False, unique=True, key='Name'))
ArticleType = mapperModel(ArticleType, table)