# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/43df8de3a5f4_dash_json.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1215 bytes
__doc__ = 'empty message\n\nRevision ID: 43df8de3a5f4\nRevises: 7dbf98566af7\nCreate Date: 2016-01-18 23:43:16.073483\n\n'
revision = '43df8de3a5f4'
down_revision = '7dbf98566af7'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dashboards', sa.Column('json_metadata', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dashboards', 'json_metadata')