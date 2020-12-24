# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/bb51420eaf83_add_schema_to_table_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1217 bytes
__doc__ = 'add schema to table model\n\nRevision ID: bb51420eaf83\nRevises: 867bf4f117f9\nCreate Date: 2016-04-11 22:41:06.185955\n\n'
revision = 'bb51420eaf83'
down_revision = '867bf4f117f9'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('schema', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('tables', 'schema')