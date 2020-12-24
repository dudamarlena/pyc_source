# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/18e88e1cc004_making_audit_nullable.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4013 bytes
__doc__ = 'making audit nullable\n\nRevision ID: 18e88e1cc004\nRevises: 430039611635\nCreate Date: 2016-03-13 21:30:24.833107\n\n'
import sqlalchemy as sa
from alembic import op
revision = '18e88e1cc004'
down_revision = '430039611635'

def upgrade():
    try:
        op.alter_column('clusters',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('clusters',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.drop_constraint(None, 'columns', type_='foreignkey')
        op.drop_constraint(None, 'columns', type_='foreignkey')
        op.drop_column('columns', 'created_on')
        op.drop_column('columns', 'created_by_fk')
        op.drop_column('columns', 'changed_on')
        op.drop_column('columns', 'changed_by_fk')
        op.alter_column('css_templates',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('css_templates',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('dashboards',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('dashboards',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.create_unique_constraint(None, 'dashboards', ['slug'])
        op.alter_column('datasources',
          'changed_by_fk', existing_type=(sa.INTEGER()), nullable=True)
        op.alter_column('datasources',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('datasources',
          'created_by_fk', existing_type=(sa.INTEGER()), nullable=True)
        op.alter_column('datasources',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('dbs', 'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('dbs', 'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('slices',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('slices',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('sql_metrics',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('sql_metrics',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('table_columns',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('table_columns',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('tables',
          'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('tables',
          'created_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('url', 'changed_on', existing_type=(sa.DATETIME()), nullable=True)
        op.alter_column('url', 'created_on', existing_type=(sa.DATETIME()), nullable=True)
    except Exception:
        pass


def downgrade():
    pass