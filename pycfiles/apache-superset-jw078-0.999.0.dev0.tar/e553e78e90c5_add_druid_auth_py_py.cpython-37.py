# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/e553e78e90c5_add_druid_auth_py_py.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1619 bytes
__doc__ = 'add_druid_auth_py.py\n\nRevision ID: e553e78e90c5\nRevises: 18dc26817ad2\nCreate Date: 2019-02-01 16:07:04.268023\n\n'
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