# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/f0fbf6129e13_adding_verbose_name_to_tablecolumn.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1276 bytes
__doc__ = 'Adding verbose_name to tablecolumn\n\nRevision ID: f0fbf6129e13\nRevises: c3a8f8611885\nCreate Date: 2016-05-01 12:21:18.331191\n\n'
revision = 'f0fbf6129e13'
down_revision = 'c3a8f8611885'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('table_columns', sa.Column('verbose_name', sa.String(length=1024), nullable=True))


def downgrade():
    op.drop_column('table_columns', 'verbose_name')