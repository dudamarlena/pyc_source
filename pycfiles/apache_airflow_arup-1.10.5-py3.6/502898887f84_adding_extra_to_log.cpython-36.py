# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/502898887f84_adding_extra_to_log.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1254 bytes
"""Adding extra to Log

Revision ID: 502898887f84
Revises: 52d714495f0
Create Date: 2015-11-03 22:50:49.794097

"""
from alembic import op
import sqlalchemy as sa
revision = '502898887f84'
down_revision = '52d714495f0'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('log', sa.Column('extra', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('log', 'extra')