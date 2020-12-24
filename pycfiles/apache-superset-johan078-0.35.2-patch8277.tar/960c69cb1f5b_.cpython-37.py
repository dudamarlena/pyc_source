# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/960c69cb1f5b_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1489 bytes
__doc__ = 'add dttm_format related fields in table_columns\n\nRevision ID: 960c69cb1f5b\nRevises: d8bc074f7aad\nCreate Date: 2016-06-16 14:15:19.573183\n\n'
revision = '960c69cb1f5b'
down_revision = '27ae655e4247'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('table_columns', sa.Column('python_date_format', sa.String(length=255), nullable=True))
    op.add_column('table_columns', sa.Column('database_expression', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('table_columns', 'python_date_format')
    op.drop_column('table_columns', 'database_expression')