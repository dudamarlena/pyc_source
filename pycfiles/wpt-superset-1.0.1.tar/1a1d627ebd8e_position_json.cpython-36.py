# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/1a1d627ebd8e_position_json.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1588 bytes
"""position_json

Revision ID: 1a1d627ebd8e
Revises: 0c5070e96b57
Create Date: 2018-08-13 11:30:07.101702

"""
from alembic import op
import sqlalchemy as sa
from superset.utils.core import MediumText
revision = '1a1d627ebd8e'
down_revision = '0c5070e96b57'

def upgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.alter_column('position_json',
          existing_type=(sa.Text()),
          type_=(MediumText()),
          existing_nullable=True)


def downgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.alter_column('position_json',
          existing_type=(MediumText()),
          type_=(sa.Text()),
          existing_nullable=True)