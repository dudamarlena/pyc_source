# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/41f5f12752f8_add_superuser_field.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1247 bytes
__doc__ = 'add superuser field\n\nRevision ID: 41f5f12752f8\nRevises: 03bc53e68815\nCreate Date: 2018-12-04 15:50:04.456875\n\n'
from alembic import op
import sqlalchemy as sa
revision = '41f5f12752f8'
down_revision = '03bc53e68815'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('superuser', (sa.Boolean()), default=False))


def downgrade():
    op.drop_column('users', 'superuser')