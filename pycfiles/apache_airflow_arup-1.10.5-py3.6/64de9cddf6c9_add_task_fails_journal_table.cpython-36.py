# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/64de9cddf6c9_add_task_fails_journal_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1697 bytes
"""add task fails journal table

Revision ID: 64de9cddf6c9
Revises: 211e584da130
Create Date: 2016-08-03 14:02:59.203021

"""
from alembic import op
import sqlalchemy as sa
revision = '64de9cddf6c9'
down_revision = '211e584da130'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('task_fail', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('task_id', sa.String(length=250), nullable=False), sa.Column('dag_id', sa.String(length=250), nullable=False), sa.Column('execution_date', (sa.DateTime()), nullable=False), sa.Column('start_date', (sa.DateTime()), nullable=True), sa.Column('end_date', (sa.DateTime()), nullable=True), sa.Column('duration', (sa.Integer()), nullable=True), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('task_fail')