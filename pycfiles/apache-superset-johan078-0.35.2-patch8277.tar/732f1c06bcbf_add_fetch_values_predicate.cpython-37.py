# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/732f1c06bcbf_add_fetch_values_predicate.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1455 bytes
__doc__ = 'add fetch values predicate\n\nRevision ID: 732f1c06bcbf\nRevises: d6db5a5cdb5d\nCreate Date: 2017-03-03 09:15:56.800930\n\n'
revision = '732f1c06bcbf'
down_revision = 'd6db5a5cdb5d'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('datasources', sa.Column('fetch_values_from', sa.String(length=100), nullable=True))
    op.add_column('tables', sa.Column('fetch_values_predicate', sa.String(length=1000), nullable=True))


def downgrade():
    op.drop_column('tables', 'fetch_values_predicate')
    op.drop_column('datasources', 'fetch_values_from')