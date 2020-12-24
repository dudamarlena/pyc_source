# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/a56c9515abdc_remove_dag_stat_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1581 bytes
__doc__ = 'Remove dag_stat table\n\nRevision ID: a56c9515abdc\nRevises: c8ffec048a3b\nCreate Date: 2018-12-27 10:27:59.715872\n\n'
from alembic import op
import sqlalchemy as sa
revision = 'a56c9515abdc'
down_revision = 'c8ffec048a3b'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('dag_stats')


def downgrade():
    op.create_table('dag_stats', sa.Column('dag_id', sa.String(length=250), nullable=False), sa.Column('state', sa.String(length=50), nullable=False), sa.Column('count', (sa.Integer()), nullable=False, default=0), sa.Column('dirty', (sa.Boolean()), nullable=False, default=False), sa.PrimaryKeyConstraint('dag_id', 'state'))