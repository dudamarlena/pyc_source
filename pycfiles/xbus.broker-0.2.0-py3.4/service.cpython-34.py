# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/model/service.py
# Compiled at: 2016-06-27 03:37:50
# Size of source mod 2**32: 572 bytes
from uuid import uuid4
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Boolean
from sqlalchemy.types import Text
from xbus.broker.model import metadata
from xbus.broker.model.types import UUID
__author__ = 'jgavrel'
service = Table('service', metadata, Column('id', UUID, default=uuid4, primary_key=True), Column('name', Unicode(length=64), index=True, unique=True), Column('is_consumer', Boolean, server_default='FALSE'), Column('description', Text))