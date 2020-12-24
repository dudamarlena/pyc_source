# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/55179c7f25c7_sqla_descr.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1200 bytes
"""sqla_descr

Revision ID: 55179c7f25c7
Revises: 315b3f4da9b0
Create Date: 2015-12-13 08:38:43.704145

"""
revision = '55179c7f25c7'
down_revision = '315b3f4da9b0'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('description', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('tables', 'description')