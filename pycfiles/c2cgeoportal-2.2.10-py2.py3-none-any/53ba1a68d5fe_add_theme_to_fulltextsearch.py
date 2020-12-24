# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/53ba1a68d5fe_add_theme_to_fulltextsearch.py
# Compiled at: 2019-04-23 07:29:02
"""Add theme to FullTextSearch

Revision ID: 53ba1a68d5fe
Revises: 5109242131ce
Create Date: 2015-08-05 14:43:30.889188
"""
from alembic import op, context
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
revision = '53ba1a68d5fe'
down_revision = '5109242131ce'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('tsearch', Column('interface_id', Integer, ForeignKey(schema + '.interface.id'), nullable=True), schema=schema)
    op.add_column('tsearch', Column('lang', String(2), nullable=True), schema=schema)
    op.add_column('tsearch', Column('actions', String, nullable=True), schema=schema)
    op.add_column('tsearch', Column('from_theme', Boolean, server_default='false'), schema=schema)
    op.create_index('tsearch_search_index', table_name='tsearch', columns=[
     'ts', 'public', 'role_id', 'interface_id', 'lang'], schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_index('tsearch_search_index', schema=schema)
    op.drop_column('tsearch', 'interface_id', schema=schema)
    op.drop_column('tsearch', 'lang', schema=schema)
    op.drop_column('tsearch', 'actions', schema=schema)
    op.drop_column('tsearch', 'from_theme', schema=schema)