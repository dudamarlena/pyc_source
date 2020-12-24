# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1a1d627ebd8e_position_json.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1588 bytes
__doc__ = 'position_json\n\nRevision ID: 1a1d627ebd8e\nRevises: 0c5070e96b57\nCreate Date: 2018-08-13 11:30:07.101702\n\n'
import sqlalchemy as sa
from alembic import op
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