# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/65903709c321_allow_dml.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1290 bytes
__doc__ = 'allow_dml\n\nRevision ID: 65903709c321\nRevises: 4500485bde7d\nCreate Date: 2016-09-15 08:48:27.284752\n\n'
import logging, sqlalchemy as sa
from alembic import op
revision = '65903709c321'
down_revision = '4500485bde7d'

def upgrade():
    op.add_column('dbs', sa.Column('allow_dml', (sa.Boolean()), nullable=True))


def downgrade():
    try:
        op.drop_column('dbs', 'allow_dml')
    except Exception as e:
        try:
            logging.exception(e)
        finally:
            e = None
            del e