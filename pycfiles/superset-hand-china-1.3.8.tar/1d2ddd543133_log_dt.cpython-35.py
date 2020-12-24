# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/1d2ddd543133_log_dt.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 389 bytes
"""log dt

Revision ID: 1d2ddd543133
Revises: d2424a248d63
Create Date: 2016-03-25 14:35:44.642576

"""
revision = '1d2ddd543133'
down_revision = 'd2424a248d63'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('logs', sa.Column('dt', sa.Date(), nullable=True))


def downgrade():
    op.drop_column('logs', 'dt')