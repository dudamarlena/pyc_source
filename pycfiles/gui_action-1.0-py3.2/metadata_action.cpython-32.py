# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/action/meta/metadata_action.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Apr 19, 2012

@package: gui action
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Meta data definition package.
"""
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sql_alchemy.support.mapper import DeclarativeMetaModel
meta = MetaData()
Base = declarative_base(metadata=meta, metaclass=DeclarativeMetaModel)