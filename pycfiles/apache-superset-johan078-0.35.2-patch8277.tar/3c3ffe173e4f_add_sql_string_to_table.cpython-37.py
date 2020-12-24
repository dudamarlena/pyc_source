# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/3c3ffe173e4f_add_sql_string_to_table.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1197 bytes
__doc__ = 'add_sql_string_to_table\n\nRevision ID: 3c3ffe173e4f\nRevises: ad82a75afd82\nCreate Date: 2016-08-18 14:06:28.784699\n\n'
revision = '3c3ffe173e4f'
down_revision = 'ad82a75afd82'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('sql', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('tables', 'sql')