# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/model/input.py
# Compiled at: 2016-06-27 03:37:38
# Size of source mod 2**32: 786 bytes
"""Ways of sending data into xbus.
"""
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy import LargeBinary
from sqlalchemy import Table
from sqlalchemy import Unicode
from xbus.broker.model import metadata
from xbus.broker.model.types import UUID
INPUT_TYPES = {'descriptor': 'input_descriptor'}
input_descriptor = Table('input_descriptor', metadata, Column('id', UUID, default=uuid4, primary_key=True), Column('name', Unicode(length=64), index=True, nullable=False, unique=True), Column('descriptor', LargeBinary, nullable=False), Column('descriptor_mimetype', Unicode(length=64)))