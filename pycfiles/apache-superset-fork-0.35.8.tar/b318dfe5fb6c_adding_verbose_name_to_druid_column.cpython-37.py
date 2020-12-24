# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b318dfe5fb6c_adding_verbose_name_to_druid_column.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1256 bytes
"""adding verbose_name to druid column

Revision ID: b318dfe5fb6c
Revises: d6db5a5cdb5d
Create Date: 2017-03-08 11:48:10.835741

"""
revision = 'b318dfe5fb6c'
down_revision = 'd6db5a5cdb5d'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('columns', sa.Column('verbose_name', sa.String(length=1024), nullable=True))


def downgrade():
    op.drop_column('columns', 'verbose_name')