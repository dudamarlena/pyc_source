# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b6fa807eac07_make_names_non_nullable.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4406 bytes
__doc__ = 'make_names_non_nullable\n\nRevision ID: b6fa807eac07\nRevises: 1495eb914ad3\nCreate Date: 2019-10-02 00:29:16.679272\n\n'
import sqlalchemy as sa
from alembic import op
from superset.utils.core import generic_find_fk_constraint_name
revision = 'b6fa807eac07'
down_revision = '1495eb914ad3'
conv = {'fk':'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s', 
 'uq':'uq_%(table_name)s_%(column_0_name)s'}

def upgrade():
    bind = op.get_bind()
    insp = sa.engine.reflection.Inspector.from_engine(bind)
    fk_datasources_cluster_name_clusters = generic_find_fk_constraint_name('datasources', {'cluster_name'}, 'clusters', insp) or 
    with op.batch_alter_table('datasources', naming_convention=conv) as (batch_op):
        batch_op.drop_constraint(fk_datasources_cluster_name_clusters,
          type_='foreignkey')
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.alter_column('cluster_name',
          existing_type=(sa.String(250)), nullable=False)
    with op.batch_alter_table('clusters') as (batch_op):
        batch_op.alter_column('cluster_name',
          existing_type=(sa.String(250)), nullable=False)
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.alter_column('database_name',
          existing_type=(sa.String(250)), nullable=False)
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.alter_column('table_name',
          existing_type=(sa.String(250)), nullable=False)
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.create_foreign_key(fk_datasources_cluster_name_clusters, 'clusters', [
         'cluster_name'], [
         'cluster_name'])


def downgrade():
    bind = op.get_bind()
    insp = sa.engine.reflection.Inspector.from_engine(bind)
    fk_datasources_cluster_name_clusters = generic_find_fk_constraint_name('datasources', {'cluster_name'}, 'clusters', insp) or 
    with op.batch_alter_table('datasources', naming_convention=conv) as (batch_op):
        batch_op.drop_constraint(fk_datasources_cluster_name_clusters,
          type_='foreignkey')
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.alter_column('cluster_name',
          existing_type=(sa.String(250)), nullable=True)
    with op.batch_alter_table('clusters') as (batch_op):
        batch_op.alter_column('cluster_name',
          existing_type=(sa.String(250)), nullable=True)
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.alter_column('database_name',
          existing_type=(sa.String(250)), nullable=True)
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.alter_column('table_name', existing_type=(sa.String(250)), nullable=True)
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.create_foreign_key(fk_datasources_cluster_name_clusters, 'clusters', [
         'cluster_name'], [
         'cluster_name'])