# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/e553e78e90c5_add_druid_auth_py_py.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1619 bytes
"""add_druid_auth_py.py

Revision ID: e553e78e90c5
Revises: 18dc26817ad2
Create Date: 2019-02-01 16:07:04.268023

"""
revision = 'e553e78e90c5'
down_revision = '18dc26817ad2'
import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import EncryptedType

def upgrade():
    op.add_column('clusters', sa.Column('broker_pass', (EncryptedType()), nullable=True))
    op.add_column('clusters', sa.Column('broker_user', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('clusters', 'broker_user')
    op.drop_column('clusters', 'broker_pass')