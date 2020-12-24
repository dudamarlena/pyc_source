# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/ec82a8906649_add_missing_on_delete_cascade_on_layer_.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Add missing on delete cascade on layer tree\n\nRevision ID: ec82a8906649\nRevises: e7e03dedade3\nCreate Date: 2016-08-30 13:43:30.969505\n'
from alembic import op, context
revision = 'ec82a8906649'
down_revision = 'e7e03dedade3'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    for source, dest in [
     ('layer_wmts', 'layer'),
     ('layerv1', 'layer'),
     ('theme', 'treegroup')]:
        op.drop_constraint(('{}_id_fkey').format(source), source, schema=schema)
        op.create_foreign_key(('{}_id_fkey').format(source), source, source_schema=schema, local_cols=['id'], referent_table=dest, referent_schema=schema, remote_cols=['id'], ondelete='cascade')


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    for source, dest in [
     ('layer_wmts', 'layer'),
     ('layerv1', 'layer'),
     ('theme', 'treegroup')]:
        op.drop_constraint(('{}_id_fkey').format(source), source, schema=schema)
        op.create_foreign_key(('{}_id_fkey').format(source), source, source_schema=schema, local_cols=['id'], referent_table=dest, referent_schema=schema, remote_cols=['id'])