# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/338e90f54d61_more_logging_into_task_isntance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1449 bytes
__doc__ = 'More logging into task_instance\n\nRevision ID: 338e90f54d61\nRevises: 13eb55f81627\nCreate Date: 2015-08-25 06:09:20.460147\n\n'
from alembic import op
import sqlalchemy as sa
revision = '338e90f54d61'
down_revision = '13eb55f81627'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('task_instance', sa.Column('operator', sa.String(length=1000), nullable=True))
    op.add_column('task_instance', sa.Column('queued_dttm', (sa.DateTime()), nullable=True))


def downgrade():
    op.drop_column('task_instance', 'queued_dttm')
    op.drop_column('task_instance', 'operator')