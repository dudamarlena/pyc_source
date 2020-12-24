# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/4446e08588_dagrun_start_end.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1396 bytes
"""dagrun start end

Revision ID: 4446e08588
Revises: 561833c1c74b
Create Date: 2015-12-10 11:26:18.439223

"""
from alembic import op
import sqlalchemy as sa
revision = '4446e08588'
down_revision = '561833c1c74b'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('dag_run', sa.Column('end_date', (sa.DateTime()), nullable=True))
    op.add_column('dag_run', sa.Column('start_date', (sa.DateTime()), nullable=True))


def downgrade():
    op.drop_column('dag_run', 'start_date')
    op.drop_column('dag_run', 'end_date')