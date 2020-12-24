# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/2e82aab8ef20_rename_user_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1198 bytes
"""rename user table

Revision ID: 2e82aab8ef20
Revises: 1968acfc09e3
Create Date: 2016-04-02 19:28:15.211915

"""
from alembic import op
revision = '2e82aab8ef20'
down_revision = '1968acfc09e3'
branch_labels = None
depends_on = None

def upgrade():
    op.rename_table('user', 'users')


def downgrade():
    op.rename_table('users', 'user')