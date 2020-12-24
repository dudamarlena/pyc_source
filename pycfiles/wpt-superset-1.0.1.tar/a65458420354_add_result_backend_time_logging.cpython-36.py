# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/a65458420354_add_result_backend_time_logging.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1320 bytes
"""add_result_backend_time_logging

Revision ID: a65458420354
Revises: 2fcdcb35e487
Create Date: 2017-04-25 10:00:58.053120

"""
from alembic import op
import sqlalchemy as sa
revision = 'a65458420354'
down_revision = '2fcdcb35e487'

def upgrade():
    op.add_column('query', sa.Column('end_result_backend_time',
      sa.Numeric(precision=20, scale=6),
      nullable=True))


def downgrade():
    op.drop_column('query', 'end_result_backend_time')