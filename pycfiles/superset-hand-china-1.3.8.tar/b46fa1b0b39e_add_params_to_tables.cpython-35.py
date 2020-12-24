# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/b46fa1b0b39e_add_params_to_tables.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 539 bytes
"""Add json_metadata to the tables table.

Revision ID: b46fa1b0b39e
Revises: ef8843b41dac
Create Date: 2016-10-05 11:30:31.748238

"""
revision = 'b46fa1b0b39e'
down_revision = 'ef8843b41dac'
from alembic import op
import logging, sqlalchemy as sa

def upgrade():
    op.add_column('tables', sa.Column('params', sa.Text(), nullable=True))


def downgrade():
    try:
        op.drop_column('tables', 'params')
    except Exception as e:
        logging.warning(str(e))