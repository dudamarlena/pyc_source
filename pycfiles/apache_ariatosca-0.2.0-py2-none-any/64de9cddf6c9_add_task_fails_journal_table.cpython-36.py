# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/64de9cddf6c9_add_task_fails_journal_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1697 bytes
__doc__ = 'add task fails journal table\n\nRevision ID: 64de9cddf6c9\nRevises: 211e584da130\nCreate Date: 2016-08-03 14:02:59.203021\n\n'
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