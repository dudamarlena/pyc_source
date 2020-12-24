# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/a9c47e2c1547_add_impersonate_user_to_dbs.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1223 bytes
__doc__ = 'add impersonate_user to dbs\n\nRevision ID: a9c47e2c1547\nRevises: ca69c70ec99b\nCreate Date: 2017-08-31 17:35:58.230723\n\n'
revision = 'a9c47e2c1547'
down_revision = 'ca69c70ec99b'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dbs', sa.Column('impersonate_user', (sa.Boolean()), nullable=True))


def downgrade():
    op.drop_column('dbs', 'impersonate_user')