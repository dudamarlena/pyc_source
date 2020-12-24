# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/d827694c7555_css_templates.py
# Compiled at: 2018-08-15 11:21:52
"""css templates

Revision ID: d827694c7555
Revises: 43df8de3a5f4
Create Date: 2016-02-03 17:41:10.944019

"""
revision = 'd827694c7555'
down_revision = '43df8de3a5f4'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('css_templates', sa.Column('created_on', sa.DateTime(), nullable=False), sa.Column('changed_on', sa.DateTime(), nullable=False), sa.Column('id', sa.Integer(), nullable=False), sa.Column('template_name', sa.String(length=250), nullable=True), sa.Column('css', sa.Text(), nullable=True), sa.Column('changed_by_fk', sa.Integer(), nullable=True), sa.Column('created_by_fk', sa.Integer(), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('css_templates')