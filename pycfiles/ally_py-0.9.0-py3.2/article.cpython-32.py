# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/support/sqlalchemy/samples/meta/article.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Aug 25, 2011

@package: ally core sql alchemy
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for article API.
"""
from . import meta
from ..api.article import Article
from .article_type import ArticleType
from ally.support.sqlalchemy.mapper import mapperModel
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.types import String, Integer
table = Table('article', meta, Column('id', Integer, primary_key=True, key='Id'), Column('fk_article_type_id', ForeignKey(ArticleType.Id), nullable=False, key='Type'), Column('name', String(255), nullable=False, key='Name'))
Article = mapperModel(Article, table)