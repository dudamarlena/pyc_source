# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/sql.py
# Compiled at: 2013-04-11 17:47:52
"""
This module complements the sqlalchemy sql module, and contains the `metadata` 
variable, which is a global :class:`sqlalchemy.Metadata` object to which all 
tables of the application can be added.
"""
import logging
from sqlalchemy import event, MetaData
import sqlalchemy.sql.operators
from camelot.core.auto_reload import auto_reload
LOGGER = logging.getLogger('camelot.core.sql')
metadata = MetaData()
metadata.autoflush = False
metadata.transactional = False
event.listen(auto_reload, 'before_reload', metadata.clear)

def like_op(column, string):
    return sqlalchemy.sql.operators.like_op(column, '%%%s%%' % string)