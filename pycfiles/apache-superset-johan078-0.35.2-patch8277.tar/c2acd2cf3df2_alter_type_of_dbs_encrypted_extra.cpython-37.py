# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/c2acd2cf3df2_alter_type_of_dbs_encrypted_extra.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2049 bytes
__doc__ = 'alter type of dbs encrypted_extra\n\n\nRevision ID: c2acd2cf3df2\nRevises: cca2f5d568c8\nCreate Date: 2019-11-01 09:18:36.953603\n\n'
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