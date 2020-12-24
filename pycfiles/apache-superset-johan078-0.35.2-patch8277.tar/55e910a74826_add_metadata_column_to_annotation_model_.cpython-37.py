# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/55e910a74826_add_metadata_column_to_annotation_model_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1244 bytes
__doc__ = 'add_metadata_column_to_annotation_model.py\n\nRevision ID: 55e910a74826\nRevises: 1a1d627ebd8e\nCreate Date: 2018-08-29 14:35:20.407743\n\n'
revision = '55e910a74826'
down_revision = '1a1d627ebd8e'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('annotation', sa.Column('json_metadata', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('annotation', 'json_metadata')