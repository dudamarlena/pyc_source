# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/2b8ed8c1df94_set_layergroup_treeitem_is_as_a_primary_.py
# Compiled at: 2019-04-23 07:29:02
"""Set layergroup_treeitem.id as a primary key

Revision ID: 2b8ed8c1df94
Revises: 26a8c51827c6
Create Date: 2015-10-29 16:11:24.760733
"""
from alembic import op, context
revision = '2b8ed8c1df94'
down_revision = '32527659d57b'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.create_primary_key('layergroup_treeitem_pkey', 'layergroup_treeitem', ['id'], schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_constraint('layergroup_treeitem_pkey', 'layergroup_treeitem', schema=schema)