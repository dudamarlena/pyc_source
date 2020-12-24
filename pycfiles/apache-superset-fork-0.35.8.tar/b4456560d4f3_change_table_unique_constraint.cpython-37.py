# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b4456560d4f3_change_table_unique_constraint.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1560 bytes
"""change_table_unique_constraint

Revision ID: b4456560d4f3
Revises: bb51420eaf83
Create Date: 2016-04-15 08:31:26.249591

"""
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