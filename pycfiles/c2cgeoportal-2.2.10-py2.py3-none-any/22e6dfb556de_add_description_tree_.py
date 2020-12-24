# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/22e6dfb556de_add_description_tree_.py
# Compiled at: 2019-04-23 07:29:02
"""Add description column in the tree

Revision ID: 22e6dfb556de
Revises: 2b8ed8c1df94
Create Date: 2015-12-04 13:44:42.475652
"""
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