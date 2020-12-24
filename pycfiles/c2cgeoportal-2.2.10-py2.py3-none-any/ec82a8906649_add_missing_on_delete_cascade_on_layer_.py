# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/ec82a8906649_add_missing_on_delete_cascade_on_layer_.py
# Compiled at: 2019-04-23 07:29:02
"""Add missing on delete cascade on layer tree

Revision ID: ec82a8906649
Revises: e7e03dedade3
Create Date: 2016-08-30 13:43:30.969505
"""
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