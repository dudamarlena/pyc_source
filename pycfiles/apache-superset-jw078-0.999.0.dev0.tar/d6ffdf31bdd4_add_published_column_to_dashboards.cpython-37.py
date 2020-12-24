# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/d6ffdf31bdd4_add_published_column_to_dashboards.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1391 bytes
__doc__ = 'Add published column to dashboards\n\nRevision ID: d6ffdf31bdd4\nRevises: b4a38aa87893\nCreate Date: 2018-03-30 14:00:44.929483\n\n'
revision = 'd6ffdf31bdd4'
down_revision = 'b4a38aa87893'
import sqlalchemy as sa
from alembic import op

def upgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.add_column(sa.Column('published', (sa.Boolean()), nullable=True))
    op.execute("UPDATE dashboards SET published='1'")


def downgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.drop_column('published')