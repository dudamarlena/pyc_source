# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/1968acfc09e3_add_is_encrypted_column_to_variable_.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1303 bytes
__doc__ = 'add is_encrypted column to variable table\n\nRevision ID: 1968acfc09e3\nRevises: bba5a7cfc896\nCreate Date: 2016-02-02 17:20:55.692295\n\n'
from alembic import op
import sqlalchemy as sa
revision = '1968acfc09e3'
down_revision = 'bba5a7cfc896'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('variable', sa.Column('is_encrypted', (sa.Boolean), default=False))


def downgrade():
    op.drop_column('variable', 'is_encrypted')