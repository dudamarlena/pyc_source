# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/action/meta/action.py
# Compiled at: 2013-11-05 09:04:27
"""
Created on Aug 19, 2013

@package: gui action
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for gui actions.
"""
from ..api.action import Action
from .metadata_action import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import String

class ActionMapped(Base, Action):
    """
    Provides the action mapping.
    """
    __tablename__ = 'gui_action'
    __table_args__ = dict(mysql_engine='InnoDB')
    Path = Column('path', String(255), primary_key=True)
    Label = Column('label', String(255))
    Script = Column('script', String(255))
    NavBar = Column('navbar', String(255))