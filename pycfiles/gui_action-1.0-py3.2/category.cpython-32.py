# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/action/meta/category.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Sep 4, 2013

@package: gui action
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for gui actions category.
"""
from .action import ActionMapped
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import Column, ForeignKey

class WithCategoryAction:
    """
    Provides the action category relation definition.
    """
    __table_args__ = dict(mysql_engine='InnoDB')
    actionPath = declared_attr(lambda cls: Column('fk_action_path', ForeignKey(ActionMapped.Path, ondelete='CASCADE'), primary_key=True))

    @declared_attr
    def categoryId(cls):
        raise Exception('A category id definition is required')