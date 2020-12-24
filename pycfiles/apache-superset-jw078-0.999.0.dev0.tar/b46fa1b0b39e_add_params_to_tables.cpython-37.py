# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/b46fa1b0b39e_add_params_to_tables.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1306 bytes
__doc__ = 'Add json_metadata to the tables table.\n\nRevision ID: b46fa1b0b39e\nRevises: ef8843b41dac\nCreate Date: 2016-10-05 11:30:31.748238\n\n'
revision = 'b46fa1b0b39e'
down_revision = 'ef8843b41dac'
import logging, sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('params', (sa.Text()), nullable=True))


def downgrade():
    try:
        op.drop_column('tables', 'params')
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e