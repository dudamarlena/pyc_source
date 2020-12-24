# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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