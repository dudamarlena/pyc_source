# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/cefabc8f7d38_increase_size_of_name_column_in_ab_view_.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1640 bytes
"""Increase size of name column in ab_view_menu

Revision ID: cefabc8f7d38
Revises: 6c7537a6004a
Create Date: 2018-12-13 15:38:36.772750

"""
revision = 'cefabc8f7d38'
down_revision = '6c7537a6004a'
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('ab_view_menu') as (batch_op):
        batch_op.alter_column('name',
          existing_type=sa.String(length=100),
          existing_nullable=False,
          type_=sa.String(length=255),
          nullable=False)


def downgrade():
    with op.batch_alter_table('ab_view_menu') as (batch_op):
        batch_op.alter_column('name',
          existing_type=sa.String(length=255),
          existing_nullable=False,
          type_=sa.String(length=100),
          nullable=False)