# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/f2ca10b85618_add_dag_stats_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1578 bytes
__doc__ = 'add dag_stats table\n\nRevision ID: f2ca10b85618\nRevises: 64de9cddf6c9\nCreate Date: 2016-07-20 15:08:28.247537\n\n'
from alembic import op
import sqlalchemy as sa
revision = 'f2ca10b85618'
down_revision = '64de9cddf6c9'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('dag_stats', sa.Column('dag_id', sa.String(length=250), nullable=False), sa.Column('state', sa.String(length=50), nullable=False), sa.Column('count', (sa.Integer()), nullable=False, default=0), sa.Column('dirty', (sa.Boolean()), nullable=False, default=False), sa.PrimaryKeyConstraint('dag_id', 'state'))


def downgrade():
    op.drop_table('dag_stats')