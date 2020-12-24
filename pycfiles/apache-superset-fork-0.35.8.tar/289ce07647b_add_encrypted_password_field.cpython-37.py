# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/289ce07647b_add_encrypted_password_field.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1282 bytes
"""Add encrypted password field

Revision ID: 289ce07647b
Revises: 2929af7925ed
Create Date: 2015-11-21 11:18:00.650587

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import EncryptedType
revision = '289ce07647b'
down_revision = '2929af7925ed'

def upgrade():
    op.add_column('dbs', sa.Column('password', (EncryptedType(sa.String(1024))), nullable=True))


def downgrade():
    op.drop_column('dbs', 'password')