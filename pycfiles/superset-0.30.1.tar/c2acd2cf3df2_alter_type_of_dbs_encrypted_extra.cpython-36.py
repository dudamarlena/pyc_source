# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/c2acd2cf3df2_alter_type_of_dbs_encrypted_extra.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 2049 bytes
"""alter type of dbs encrypted_extra

Revision ID: c2acd2cf3df2
Revises: cca2f5d568c8
Create Date: 2019-11-01 09:18:36.953603

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import EncryptedType
revision = 'c2acd2cf3df2'
down_revision = 'cca2f5d568c8'

def upgrade():
    with op.batch_alter_table('dbs') as (batch_op):
        try:
            batch_op.alter_column('encrypted_extra',
              existing_type=(sa.Text()),
              type_=(EncryptedType(sa.Text())),
              postgresql_using='encrypted_extra::bytea',
              existing_nullable=True)
        except TypeError:
            batch_op.alter_column('dbs',
              'encrypted_extra',
              existing_type=(sa.Text()),
              type_=(EncryptedType(sa.Text())),
              existing_nullable=True)


def downgrade():
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.alter_column('encrypted_extra',
          existing_type=(EncryptedType(sa.Text())),
          type_=(sa.Text()),
          existing_nullable=True)