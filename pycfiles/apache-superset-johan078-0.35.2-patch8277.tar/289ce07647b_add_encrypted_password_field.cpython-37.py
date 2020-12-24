# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/289ce07647b_add_encrypted_password_field.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1282 bytes
__doc__ = 'Add encrypted password field\n\nRevision ID: 289ce07647b\nRevises: 2929af7925ed\nCreate Date: 2015-11-21 11:18:00.650587\n\n'
import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import EncryptedType
revision = '289ce07647b'
down_revision = '2929af7925ed'

def upgrade():
    op.add_column('dbs', sa.Column('password', (EncryptedType(sa.String(1024))), nullable=True))


def downgrade():
    op.drop_column('dbs', 'password')