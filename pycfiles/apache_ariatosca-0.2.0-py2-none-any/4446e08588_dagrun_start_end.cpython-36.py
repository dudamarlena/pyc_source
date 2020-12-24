# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/4446e08588_dagrun_start_end.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1396 bytes
__doc__ = 'dagrun start end\n\nRevision ID: 4446e08588\nRevises: 561833c1c74b\nCreate Date: 2015-12-10 11:26:18.439223\n\n'
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