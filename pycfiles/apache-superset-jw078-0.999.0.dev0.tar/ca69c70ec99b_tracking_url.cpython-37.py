# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/ca69c70ec99b_tracking_url.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1240 bytes
__doc__ = 'tracking_url\n\nRevision ID: ca69c70ec99b\nRevises: a65458420354\nCreate Date: 2017-07-26 20:09:52.606416\n\n'
revision = 'ca69c70ec99b'
down_revision = 'a65458420354'
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('query', sa.Column('tracking_url', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('query', 'tracking_url')