# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\audit_mixin.py
# Compiled at: 2020-03-12 16:37:30
# Size of source mod 2**32: 1641 bytes
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from flask_security import current_user

class AuditMixin(object):
    created_at = Column(DateTime, default=(datetime.now))
    updated_at = Column(DateTime, default=(datetime.now), onupdate=(datetime.now))


def _current_user_id_or_none():
    try:
        return current_user.id
    except:
        return