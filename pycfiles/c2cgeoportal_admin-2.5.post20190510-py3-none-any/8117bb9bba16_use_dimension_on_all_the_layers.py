# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/8117bb9bba16_use_dimension_on_all_the_layers.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Use dimension on all the layers\n\nRevision ID: 8117bb9bba16\nRevises: daf738d5bae4\nCreate Date: 2016-08-16 16:53:07.012668\n'
from alembic import op, context
revision = '8117bb9bba16'
down_revision = 'b60f2a505f42'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.rename_table('wmts_dimension', 'dimension', schema=schema)
    with op.batch_alter_table('dimension', schema=schema) as (table_op):
        table_op.drop_constraint('wmts_dimension_layer_id_fkey', type_='foreignkey')
        table_op.create_foreign_key('dimension_layer_id_fkey', local_cols=['layer_id'], referent_schema=schema, referent_table='layer', remote_cols=['id'])


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    with op.batch_alter_table('dimension', schema=schema) as (table_op):
        table_op.drop_constraint('dimension_layer_id_fkey', type_='foreignkey')
        table_op.create_foreign_key('wmts_dimension_layer_id_fkey', local_cols=['layer_id'], referent_schema=schema, referent_table='layer_wmts', remote_cols=['id'])
    op.rename_table('dimension', 'wmts_dimension', schema=schema)