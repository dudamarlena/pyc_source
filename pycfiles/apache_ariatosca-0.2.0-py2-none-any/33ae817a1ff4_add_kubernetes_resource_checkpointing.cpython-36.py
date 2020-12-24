# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/33ae817a1ff4_add_kubernetes_resource_checkpointing.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2010 bytes
__doc__ = 'kubernetes_resource_checkpointing\n\nRevision ID: 33ae817a1ff4\nRevises: 947454bf1dff\nCreate Date: 2017-09-11 15:26:47.598494\n\n'
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