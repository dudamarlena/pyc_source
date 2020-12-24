# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/54645a535ad6_add_ordering_in_relation.py
# Compiled at: 2019-04-23 07:29:02
"""Add ordering in relation

Revision ID: 54645a535ad6
Revises: 415746eb9f6
Create Date: 2014-11-25 14:39:05.110315
"""
from alembic import op, context
from sqlalchemy import Column
from sqlalchemy.types import Integer
revision = '54645a535ad6'
down_revision = '415746eb9f6'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_constraint('layergroup_treeitem_pkey', 'layergroup_treeitem', schema=schema)
    op.add_column('layergroup_treeitem', Column('id', Integer, primary_key=True), schema=schema)
    op.add_column('layergroup_treeitem', Column('ordering', Integer), schema=schema)
    op.execute('UPDATE ONLY %(schema)s.layergroup_treeitem AS lt SET ordering = ti."order" FROM %(schema)s.treeitem AS ti WHERE ti.id = lt.treeitem_id ' % {'schema': schema})
    op.add_column('theme', Column('ordering', Integer), schema=schema)
    op.execute('UPDATE ONLY %(schema)s.theme AS t SET ordering = ti."order" FROM %(schema)s.treeitem AS ti WHERE ti.id = t.id ' % {'schema': schema})
    op.drop_column('treeitem', 'order', schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('treeitem', Column('order', Integer), schema=schema)
    op.execute('UPDATE ONLY %(schema)s.treeitem AS ti SET "order" = lt.ordering FROM %(schema)s.layergroup_treeitem AS lt WHERE ti.id = lt.treeitem_id ' % {'schema': schema})
    op.execute('UPDATE ONLY %(schema)s.treeitem AS ti SET "order" = t.ordering FROM %(schema)s.theme AS t WHERE ti.id = t.id ' % {'schema': schema})
    op.drop_column('theme', 'ordering', schema=schema)
    op.drop_column('layergroup_treeitem', 'ordering', schema=schema)
    op.drop_column('layergroup_treeitem', 'id', schema=schema)
    op.create_primary_key('layergroup_treeitem_pkey', 'layergroup_treeitem', [
     'treegroup_id', 'treeitem_id'], schema=schema)