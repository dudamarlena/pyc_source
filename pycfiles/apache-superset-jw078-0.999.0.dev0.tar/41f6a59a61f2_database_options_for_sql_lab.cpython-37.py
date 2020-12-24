# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/41f6a59a61f2_database_options_for_sql_lab.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1499 bytes
__doc__ = 'database options for sql lab\n\nRevision ID: 41f6a59a61f2\nRevises: 3c3ffe173e4f\nCreate Date: 2016-08-31 10:26:37.969107\n\n'
import sqlalchemy as sa
from alembic import op
revision = '41f6a59a61f2'
down_revision = '3c3ffe173e4f'

def upgrade():
    op.add_column('dbs', sa.Column('allow_ctas', (sa.Boolean()), nullable=True))
    op.add_column('dbs', sa.Column('expose_in_sqllab', (sa.Boolean()), nullable=True))
    op.add_column('dbs', sa.Column('force_ctas_schema', sa.String(length=250), nullable=True))


def downgrade():
    op.drop_column('dbs', 'force_ctas_schema')
    op.drop_column('dbs', 'expose_in_sqllab')
    op.drop_column('dbs', 'allow_ctas')