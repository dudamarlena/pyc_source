# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/86770d1215c0_add_kubernetes_scheduler_uniqueness.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1978 bytes
"""add kubernetes scheduler uniqueness

Revision ID: 86770d1215c0
Revises: 27c6a30d7c24
Create Date: 2018-04-03 15:31:20.814328

"""
from alembic import op
import sqlalchemy as sa
revision = '86770d1215c0'
down_revision = '27c6a30d7c24'
branch_labels = None
depends_on = None
RESOURCE_TABLE = 'kube_worker_uuid'

def upgrade():
    columns_and_constraints = [
     sa.Column('one_row_id', (sa.Boolean), server_default=(sa.true()), primary_key=True),
     sa.Column('worker_uuid', sa.String(255))]
    conn = op.get_bind()
    if conn.dialect.name in 'mysql':
        columns_and_constraints.append(sa.CheckConstraint('one_row_id<>0', name='kube_worker_one_row_id'))
    else:
        if conn.dialect.name not in 'mssql':
            columns_and_constraints.append(sa.CheckConstraint('one_row_id', name='kube_worker_one_row_id'))
    table = (op.create_table)(RESOURCE_TABLE, *columns_and_constraints)
    op.bulk_insert(table, [
     {'worker_uuid': ''}])


def downgrade():
    op.drop_table(RESOURCE_TABLE)