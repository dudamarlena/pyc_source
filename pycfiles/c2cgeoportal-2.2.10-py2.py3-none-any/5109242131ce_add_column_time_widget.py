# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/5109242131ce_add_column_time_widget.py
# Compiled at: 2019-04-23 07:29:02
"""add column time_widget

Revision ID: 5109242131ce
Revises: 164ac0819a61
Create Date: 2015-04-27 17:31:41.760977
"""
from alembic import op, context
from sqlalchemy import Column
from sqlalchemy.types import Unicode
revision = '5109242131ce'
down_revision = '164ac0819a61'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    for table in ['layerv1', 'layer_internal_wms', 'layer_external_wms']:
        op.add_column(table, Column('time_widget', Unicode(10), default='slider'), schema=schema)
        op.execute(("UPDATE {schema!s}.{table!s} SET time_widget = 'slider'").format(schema=schema, table=table))


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    for table in ['layerv1', 'layer_internal_wms', 'layer_external_wms']:
        op.drop_column(table, 'time_widget', schema=schema)