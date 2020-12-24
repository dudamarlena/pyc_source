# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/2e82aab8ef20_rename_user_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1198 bytes
__doc__ = 'rename user table\n\nRevision ID: 2e82aab8ef20\nRevises: 1968acfc09e3\nCreate Date: 2016-04-02 19:28:15.211915\n\n'
from alembic import op
revision = '2e82aab8ef20'
down_revision = '1968acfc09e3'
branch_labels = None
depends_on = None

def upgrade():
    op.rename_table('user', 'users')


def downgrade():
    op.rename_table('users', 'user')