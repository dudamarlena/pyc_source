# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/40e67319e3a9_dagrun_config.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1262 bytes
__doc__ = 'dagrun_config\n\nRevision ID: 40e67319e3a9\nRevises: 2e541a1dcfed\nCreate Date: 2015-10-29 08:36:31.726728\n\n'
from alembic import op
import sqlalchemy as sa
revision = '40e67319e3a9'
down_revision = '2e541a1dcfed'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('dag_run', sa.Column('conf', (sa.PickleType()), nullable=True))


def downgrade():
    op.drop_column('dag_run', 'conf')