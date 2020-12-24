# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1d9e835a84f9_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1364 bytes
__doc__ = 'empty message\n\nRevision ID: 1d9e835a84f9\nRevises: 3dda56f1c4c6\nCreate Date: 2018-07-16 18:04:07.764659\n\n'
import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import expression
revision = '1d9e835a84f9'
down_revision = '3dda56f1c4c6'

def upgrade():
    op.add_column('dbs', sa.Column('allow_csv_upload',
      (sa.Boolean()),
      nullable=False,
      server_default=(expression.true())))


def downgrade():
    op.drop_column('dbs', 'allow_csv_upload')