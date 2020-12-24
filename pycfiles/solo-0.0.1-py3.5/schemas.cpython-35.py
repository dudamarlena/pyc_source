# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/server/schemas.py
# Compiled at: 2016-03-02 19:33:50
# Size of source mod 2**32: 517 bytes
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
metadata = sa.MetaData()
TraitsTbl = sa.Table('traits', metadata, sa.Column('id', sa.Integer, primary_key=True), sa.Column('name', sa.String(140), nullable=False, index=True))
PeopleTbl = sa.Table('people', metadata, sa.Column('id', sa.Integer, primary_key=True), sa.Column('name', sa.String(140), nullable=False, index=True), sa.Column('traits', ARRAY(sa.Integer, dimensions=1), nullable=False, server_default='{}'))