# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/action/meta/category_right.py
# Compiled at: 2013-10-23 08:11:12
"""
Created on Sep 4, 2013

@package: gui action
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for gui right actions.
"""
from .category import WithCategoryAction
from .metadata_action import Base
from sqlalchemy.schema import Column, ForeignKey
from security.meta.right import RightMapped

class RightAction(Base, WithCategoryAction):
    """
    Provides the Right to Action mapping.
    """
    __tablename__ = 'gui_action_right'
    categoryId = Column('fk_right_id', ForeignKey(RightMapped.Id, ondelete='CASCADE'), primary_key=True)