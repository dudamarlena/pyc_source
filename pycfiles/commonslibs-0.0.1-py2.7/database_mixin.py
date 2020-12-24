# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/database_mixin.py
# Compiled at: 2015-04-04 05:19:06
from sqlalchemy import Column, BigInteger, Boolean
from app.commons import dateutil
__author__ = 'freeway'

class IdMixin(object):
    id = Column(BigInteger, primary_key=True)


class CreatedAtMixin(object):
    created_at = Column(BigInteger)


class UpdatedAtMixin(object):
    updated_at = Column(BigInteger)


class IsDeletedMixin(object):
    is_deleted = Column(Boolean, default=False)