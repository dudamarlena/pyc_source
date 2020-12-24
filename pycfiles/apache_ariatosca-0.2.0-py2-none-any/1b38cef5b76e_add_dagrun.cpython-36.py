# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/1b38cef5b76e_add_dagrun.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1843 bytes
__doc__ = 'add dagrun\n\nRevision ID: 1b38cef5b76e\nRevises: 52d714495f0\nCreate Date: 2015-10-27 08:31:48.475140\n\n'
from alembic import op
import sqlalchemy as sa
revision = '1b38cef5b76e'
down_revision = '502898887f84'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('dag_run', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('dag_id', sa.String(length=250), nullable=True), sa.Column('execution_date', (sa.DateTime()), nullable=True), sa.Column('state', sa.String(length=50), nullable=True), sa.Column('run_id', sa.String(length=250), nullable=True), sa.Column('external_trigger', (sa.Boolean()), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('dag_id', 'execution_date'), sa.UniqueConstraint('dag_id', 'run_id'))


def downgrade():
    op.drop_table('dag_run')