# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/sql.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nThis module complements the sqlalchemy sql module, and contains the `metadata` \nvariable, which is a global :class:`sqlalchemy.Metadata` object to which all \ntables of the application can be added.\n'
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