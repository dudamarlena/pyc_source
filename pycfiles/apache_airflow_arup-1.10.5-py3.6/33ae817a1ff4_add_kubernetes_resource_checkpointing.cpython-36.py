# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/33ae817a1ff4_add_kubernetes_resource_checkpointing.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2010 bytes
"""kubernetes_resource_checkpointing

Revision ID: 33ae817a1ff4
Revises: 947454bf1dff
Create Date: 2017-09-11 15:26:47.598494

"""
from alembic import op
import sqlalchemy as sa
revision = '33ae817a1ff4'
down_revision = 'd2ae31099d61'
branch_labels = None
depends_on = None
RESOURCE_TABLE = 'kube_resource_version'

def upgrade():
    columns_and_constraints = [
     sa.Column('one_row_id', (sa.Boolean), server_default=(sa.true()), primary_key=True),
     sa.Column('resource_version', sa.String(255))]
    conn = op.get_bind()
    if conn.dialect.name in 'mysql':
        columns_and_constraints.append(sa.CheckConstraint('one_row_id<>0', name='kube_resource_version_one_row_id'))
    else:
        if conn.dialect.name not in 'mssql':
            columns_and_constraints.append(sa.CheckConstraint('one_row_id', name='kube_resource_version_one_row_id'))
    table = (op.create_table)(RESOURCE_TABLE, *columns_and_constraints)
    op.bulk_insert(table, [
     {'resource_version': ''}])


def downgrade():
    op.drop_table(RESOURCE_TABLE)