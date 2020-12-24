# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/e46f2d27a08e_materialize_perms.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1469 bytes
__doc__ = 'materialize perms\n\nRevision ID: e46f2d27a08e\nRevises: c611f2b591b8\nCreate Date: 2016-11-14 15:23:32.594898\n\n'
revision = 'e46f2d27a08e'
down_revision = 'c611f2b591b8'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('datasources', sa.Column('perm', sa.String(length=1000), nullable=True))
    op.add_column('dbs', sa.Column('perm', sa.String(length=1000), nullable=True))
    op.add_column('tables', sa.Column('perm', sa.String(length=1000), nullable=True))


def downgrade():
    op.drop_column('tables', 'perm')
    op.drop_column('datasources', 'perm')
    op.drop_column('dbs', 'perm')