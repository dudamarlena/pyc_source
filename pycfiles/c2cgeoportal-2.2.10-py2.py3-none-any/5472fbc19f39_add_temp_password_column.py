# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/static/versions/5472fbc19f39_add_temp_password_column.py
# Compiled at: 2019-04-23 07:29:02
"""Add temp_password column

Revision ID: 5472fbc19f39
Revises: 1da396a88908
Create Date: 2015-04-20 14:51:30.595467
"""
from alembic import op, context
from sqlalchemy import Column, Unicode
revision = '5472fbc19f39'
down_revision = '1da396a88908'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    staticschema = schema + '_static'
    op.add_column('user', Column('temp_password', Unicode), schema=staticschema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    staticschema = schema + '_static'
    op.drop_column('user', 'temp_password', schema=staticschema)