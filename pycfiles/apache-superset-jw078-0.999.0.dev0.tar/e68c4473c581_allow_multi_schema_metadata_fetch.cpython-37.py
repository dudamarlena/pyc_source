# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/e68c4473c581_allow_multi_schema_metadata_fetch.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1360 bytes
__doc__ = 'allow_multi_schema_metadata_fetch\n\nRevision ID: e68c4473c581\nRevises: e866bd2d4976\nCreate Date: 2018-03-06 12:24:30.896293\n\n'
import sqlalchemy as sa
from alembic import op
revision = 'e68c4473c581'
down_revision = 'e866bd2d4976'

def upgrade():
    op.add_column('dbs', sa.Column('allow_multi_schema_metadata_fetch',
      (sa.Boolean()),
      nullable=True,
      default=True))


def downgrade():
    op.drop_column('dbs', 'allow_multi_schema_metadata_fetch')