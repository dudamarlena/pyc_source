# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/164ac0819a61_add_image_format_to_wmts_layer.py
# Compiled at: 2019-04-23 07:29:02
"""Add image format to WMTS layer

Revision ID: 164ac0819a61
Revises: 20137477bd02
Create Date: 2015-03-06 09:08:05.754746
"""
from alembic import op, context
from sqlalchemy import Column, Unicode
revision = '164ac0819a61'
down_revision = '20137477bd02'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('layer_wmts', Column('image_type', Unicode(10)), schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.drop_column('layer_wmts', 'image_type', schema=schema)