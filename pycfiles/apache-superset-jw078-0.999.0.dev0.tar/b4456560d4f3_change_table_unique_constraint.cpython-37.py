# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b4456560d4f3_change_table_unique_constraint.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1560 bytes
__doc__ = 'change_table_unique_constraint\n\nRevision ID: b4456560d4f3\nRevises: bb51420eaf83\nCreate Date: 2016-04-15 08:31:26.249591\n\n'
from alembic import op
revision = 'b4456560d4f3'
down_revision = 'bb51420eaf83'

def upgrade():
    try:
        op.drop_constraint('tables_table_name_key', 'tables', type_='unique')
        op.create_unique_constraint('_customer_location_uc', 'tables', ['database_id', 'schema', 'table_name'])
    except Exception:
        pass


def downgrade():
    try:
        op.drop_constraint('_customer_location_uc', 'tables', type_='unique')
    except Exception:
        pass