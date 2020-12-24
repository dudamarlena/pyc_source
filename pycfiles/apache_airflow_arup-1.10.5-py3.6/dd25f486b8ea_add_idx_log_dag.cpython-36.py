# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/dd25f486b8ea_add_idx_log_dag.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1218 bytes
from alembic import op
revision = 'dd25f486b8ea'
down_revision = '9635ae0956e7'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('idx_log_dag', 'log', ['dag_id'], unique=False)


def downgrade():
    op.drop_index('idx_log_dag', table_name='log')