# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/bcf3126872fc_add_keyvalue.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1504 bytes
__doc__ = 'Add keyvalue table\n\nRevision ID: bcf3126872fc\nRevises: f18570e03440\nCreate Date: 2017-01-10 11:47:56.306938\n\n'
revision = 'bcf3126872fc'
down_revision = 'f18570e03440'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('keyvalue', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('value', (sa.Text()), nullable=False), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('keyvalue')