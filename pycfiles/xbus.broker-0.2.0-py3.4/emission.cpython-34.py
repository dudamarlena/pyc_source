# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/model/emission.py
# Compiled at: 2016-06-27 03:37:50
# Size of source mod 2**32: 1887 bytes
"""Data emission into xbus.
"""
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Unicode
from xbus.broker.model import metadata
from xbus.broker.model.input import INPUT_TYPES
from xbus.broker.model.types import UUID
__author__ = 'faide'
emission_profile = Table('emission_profile', metadata, Column('id', UUID, default=uuid4, primary_key=True), Column('name', Unicode(length=64), index=True, nullable=False, unique=True), Column('owner_id', UUID, ForeignKey('user.user_id', ondelete='RESTRICT')), Column('input_type', Enum(*INPUT_TYPES.keys(), name='input_type'), nullable=False), Column('input_descriptor_id', UUID, ForeignKey('input_descriptor.id', ondelete='RESTRICT')), Column('encoding', Unicode, nullable=False, default='utf-8'))
emitter_profile = Table('emitter_profile', metadata, Column('id', UUID, default=uuid4, primary_key=True), Column('name', Unicode(length=64), index=True, nullable=False, unique=True), Column('display_name', Unicode(255)), Column('description', Text))
emitter_profile_event_type_rel = Table('emitter_profile_event_type_rel', metadata, Column('event_id', UUID, ForeignKey('event_type.id', ondelete='CASCADE'), primary_key=True), Column('profile_id', UUID, ForeignKey('emitter_profile.id', ondelete='CASCADE'), primary_key=True))