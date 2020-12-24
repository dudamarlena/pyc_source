# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b318dfe5fb6c_adding_verbose_name_to_druid_column.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1256 bytes
__doc__ = 'adding verbose_name to druid column\n\nRevision ID: b318dfe5fb6c\nRevises: d6db5a5cdb5d\nCreate Date: 2017-03-08 11:48:10.835741\n\n'
revision = 'b318dfe5fb6c'
down_revision = 'd6db5a5cdb5d'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('columns', sa.Column('verbose_name', sa.String(length=1024), nullable=True))


def downgrade():
    op.drop_column('columns', 'verbose_name')