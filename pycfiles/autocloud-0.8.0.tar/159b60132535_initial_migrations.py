# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/autocloud/alembic/versions/159b60132535_initial_migrations.py
# Compiled at: 2016-05-27 13:17:50
"""Initial migrations.

Revision ID: 159b60132535
Revises: 
Create Date: 2015-12-04 21:53:17.278656

"""
revision = '159b60132535'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('job_details', sa.Column('id', sa.Integer(), nullable=False), sa.Column('taskid', sa.String(length=255), nullable=False), sa.Column('status', sa.String(length=255), nullable=True), sa.Column('output', sa.Text(), nullable=False), sa.Column('created_on', sa.DateTime(), nullable=True), sa.Column('last_updated', sa.DateTime(), nullable=True), sa.Column('user', sa.String(length=255), nullable=False), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('job_details')