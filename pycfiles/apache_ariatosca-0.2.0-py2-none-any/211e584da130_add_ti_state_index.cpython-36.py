# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/211e584da130_add_ti_state_index.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1257 bytes
__doc__ = 'add TI state index\n\nRevision ID: 211e584da130\nRevises: 2e82aab8ef20\nCreate Date: 2016-06-30 10:54:24.323588\n\n'
from alembic import op
revision = '211e584da130'
down_revision = '2e82aab8ef20'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('ti_state', 'task_instance', ['state'], unique=False)


def downgrade():
    op.drop_index('ti_state', table_name='task_instance')