# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/22e6dfb556de_add_description_tree_.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Add description column in the tree\n\nRevision ID: 22e6dfb556de\nRevises: 2b8ed8c1df94\nCreate Date: 2015-12-04 13:44:42.475652\n'
from alembic import op, context
from sqlalchemy import Column, Unicode
revision = '22e6dfb556de'
down_revision = '2b8ed8c1df94'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('layergroup_treeitem', Column('description', Unicode), schema=schema)
    op.add_column('treeitem', Column('description', Unicode), schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_column('layergroup_treeitem', 'description', schema=schema)
    op.drop_column('treeitem', 'description', schema=schema)