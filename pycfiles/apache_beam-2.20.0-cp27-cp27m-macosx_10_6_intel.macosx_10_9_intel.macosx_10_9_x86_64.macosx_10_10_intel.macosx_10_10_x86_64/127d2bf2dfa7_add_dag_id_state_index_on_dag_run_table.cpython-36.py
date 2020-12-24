# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/127d2bf2dfa7_add_dag_id_state_index_on_dag_run_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1260 bytes
__doc__ = 'Add dag_id/state index on dag_run table\n\nRevision ID: 127d2bf2dfa7\nRevises: 5e7d17757c7a\nCreate Date: 2017-01-25 11:43:51.635667\n\n'
from alembic import op
revision = '127d2bf2dfa7'
down_revision = '5e7d17757c7a'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('dag_id_state', 'dag_run', ['dag_id', 'state'], unique=False)


def downgrade():
    op.drop_index('dag_id_state', table_name='dag_run')