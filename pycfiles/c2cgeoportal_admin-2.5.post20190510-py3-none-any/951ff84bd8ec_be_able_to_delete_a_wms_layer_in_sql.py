# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/951ff84bd8ec_be_able_to_delete_a_wms_layer_in_sql.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Be able to delete a WMS layer in SQL\n\nRevision ID: 951ff84bd8ec\nRevises: 29f2a32859ec\nCreate Date: 2016-06-22 15:29:24.210097\n'
from alembic import op, context
revision = '951ff84bd8ec'
down_revision = '29f2a32859ec'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_constraint('layergroup_treeitem_treeitem_id_fkey', 'layergroup_treeitem', schema=schema)
    op.create_foreign_key('layergroup_treeitem_treeitem_id_fkey', 'layergroup_treeitem', source_schema=schema, local_cols=['treeitem_id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'], ondelete='cascade')
    op.drop_constraint('treegroup_id_fkey', 'treegroup', schema=schema)
    op.create_foreign_key('treegroup_id_fkey', 'treegroup', source_schema=schema, local_cols=['id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'], ondelete='cascade')
    op.drop_constraint('ui_metadata_item_id_fkey', 'ui_metadata', schema=schema)
    op.create_foreign_key('ui_metadata_item_id_fkey', 'ui_metadata', source_schema=schema, local_cols=['item_id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'], ondelete='cascade')
    op.drop_constraint('layer_id_fkey', 'layer', schema=schema)
    op.create_foreign_key('layer_id_fkey', 'layer', source_schema=schema, local_cols=['id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'], ondelete='cascade')
    op.drop_constraint('layergroup_id_fkey', 'layergroup', schema=schema)
    op.create_foreign_key('layergroup_id_fkey', 'layergroup', source_schema=schema, local_cols=['id'], referent_table='treegroup', referent_schema=schema, remote_cols=['id'], ondelete='cascade')
    op.drop_constraint('interface_layer_layer_id_fkey', 'interface_layer', schema=schema)
    op.create_foreign_key('interface_layer_layer_id_fkey', 'interface_layer', source_schema=schema, local_cols=['layer_id'], referent_table='layer', referent_schema=schema, remote_cols=['id'], ondelete='cascade')
    op.drop_constraint('layer_wms_id_fkey', 'layer_wms', schema=schema)
    op.create_foreign_key('layer_wms_id_fkey', 'layer_wms', source_schema=schema, local_cols=['id'], referent_table='layer', referent_schema=schema, remote_cols=['id'], ondelete='cascade')


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_constraint('layergroup_treeitem_treeitem_id_fkey', 'layergroup_treeitem', schema=schema)
    op.create_foreign_key('layergroup_treeitem_treeitem_id_fkey', 'layergroup_treeitem', source_schema=schema, local_cols=['treeitem_id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'])
    op.drop_constraint('treegroup_id_fkey', 'treegroup', schema=schema)
    op.create_foreign_key('treegroup_id_fkey', 'treegroup', source_schema=schema, local_cols=['id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'])
    op.drop_constraint('ui_metadata_item_id_fkey', 'ui_metadata', schema=schema)
    op.create_foreign_key('ui_metadata_item_id_fkey', 'ui_metadata', source_schema=schema, local_cols=['item_id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'])
    op.drop_constraint('layer_id_fkey', 'layer', schema=schema)
    op.create_foreign_key('layer_id_fkey', 'layer', source_schema=schema, local_cols=['id'], referent_table='treeitem', referent_schema=schema, remote_cols=['id'])
    op.drop_constraint('layergroup_id_fkey', 'layergroup', schema=schema)
    op.create_foreign_key('layergroup_id_fkey', 'layergroup', source_schema=schema, local_cols=['id'], referent_table='treegroup', referent_schema=schema, remote_cols=['id'])
    op.drop_constraint('interface_layer_layer_id_fkey', 'interface_layer', schema=schema)
    op.create_foreign_key('interface_layer_layer_id_fkey', 'interface_layer', source_schema=schema, local_cols=['layer_id'], referent_table='layer', referent_schema=schema, remote_cols=['id'])
    op.drop_constraint('layer_wms_id_fkey', 'layer_wms', schema=schema)
    op.create_foreign_key('layer_wms_id_fkey', 'layer_wms', source_schema=schema, local_cols=['id'], referent_table='layer', referent_schema=schema, remote_cols=['id'])