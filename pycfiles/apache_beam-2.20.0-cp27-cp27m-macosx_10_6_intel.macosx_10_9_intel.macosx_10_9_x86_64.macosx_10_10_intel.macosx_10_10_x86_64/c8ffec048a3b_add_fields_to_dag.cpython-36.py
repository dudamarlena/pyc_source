# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/c8ffec048a3b_add_fields_to_dag.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1367 bytes
__doc__ = 'add fields to dag\n\nRevision ID: c8ffec048a3b\nRevises: 41f5f12752f8\nCreate Date: 2018-12-23 21:55:46.463634\n\n'
from alembic import op
import sqlalchemy as sa
revision = 'c8ffec048a3b'
down_revision = '41f5f12752f8'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('dag', sa.Column('description', (sa.Text()), nullable=True))
    op.add_column('dag', sa.Column('default_view', (sa.String(25)), nullable=True))


def downgrade():
    op.drop_column('dag', 'description')
    op.drop_column('dag', 'default_view')