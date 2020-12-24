# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/7d271f4527cd_add_layer_column_in_layerv1_table.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Add layer column in layerv1 table\n\nRevision ID: 7d271f4527cd\nRevises: 8117bb9bba16\nCreate Date: 2016-10-20 15:00:13.619090\n'
from alembic import op, context
from sqlalchemy import Column
from sqlalchemy.types import Unicode
revision = '7d271f4527cd'
down_revision = '8117bb9bba16'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('layerv1', Column('layer', Unicode), schema=schema)
    op.execute(('UPDATE {schema}.layerv1 AS l1 SET layer = name FROM {schema}.treeitem AS ti WHERE l1.id = ti.id').format(schema=schema))


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_column('layerv1', 'layer', schema=schema)