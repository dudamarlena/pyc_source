# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\c611f2b591b8_dim_spec.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1216 bytes
"""dim_spec

Revision ID: c611f2b591b8
Revises: ad4d656d92bc
Create Date: 2016-11-02 17:36:04.970448

"""
revision = 'c611f2b591b8'
down_revision = 'ad4d656d92bc'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('columns', sa.Column('dimension_spec_json', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('columns', 'dimension_spec_json')