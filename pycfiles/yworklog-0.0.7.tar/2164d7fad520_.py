# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: alembic/versions/2164d7fad520_.py
# Compiled at: 2013-03-19 22:52:41
"""empty message

Revision ID: 2164d7fad520
Revises: 3876f3c32a4a
Create Date: 2012-10-13 04:13:08.040685

"""
revision = '2164d7fad520'
down_revision = '3876f3c32a4a'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('start_attrs', sa.Column('id', sa.Integer(), nullable=False), sa.Column('worklog_id', sa.Integer(), nullable=True), sa.Column('project', sa.String(length=256), nullable=True), sa.Column('ref', sa.Integer(), nullable=True), sa.ForeignKeyConstraint(['worklog_id'], ['worklog.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('start_attrs')