# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/1d5d4abfebd1_add_restricted_theme.py
# Compiled at: 2019-04-23 07:29:02
"""Add restricted theme

Revision ID: 1d5d4abfebd1
Revises: 54645a535ad6
Create Date: 2014-11-25 16:51:51.567026
"""
from alembic import op, context
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Boolean
revision = '1d5d4abfebd1'
down_revision = '54645a535ad6'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    engine = op.get_bind().engine
    if type(engine).__name__ != 'MockConnection' and op.get_context().dialect.has_table(engine, 'restricted_role_theme', schema=schema):
        return
    op.add_column('theme', Column('public', Boolean, server_default='t', nullable=False), schema=schema)
    op.create_table('restricted_role_theme', Column('role_id', Integer, ForeignKey(schema + '.role.id'), primary_key=True), Column('theme_id', Integer, ForeignKey(schema + '.theme.id'), primary_key=True), schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_table('restricted_role_theme', schema=schema)
    op.drop_column('theme', 'public', schema=schema)