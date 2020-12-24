# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/6a412d9437b1_rename_serverogc_to_ogcserver.py
# Compiled at: 2019-04-23 07:29:02
"""Rename ServerOGC to OGCServer

Revision ID: 6a412d9437b1
Revises: 29f2a32859ec
Create Date: 2016-06-28 18:08:23.888198
"""
from alembic import op, context
revision = '6a412d9437b1'
down_revision = '29f2a32859ec'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.rename_table('server_ogc', 'ogc_server', schema=schema)
    with op.batch_alter_table('layer_wms', schema=schema) as (table_op):
        table_op.alter_column('server_ogc_id', new_column_name='ogc_server_id')


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.rename_table('ogc_server', 'server_ogc', schema=schema)
    with op.batch_alter_table('layer_wms', schema=schema) as (table_op):
        table_op.alter_column('ogc_server_id', new_column_name='server_ogc_id')