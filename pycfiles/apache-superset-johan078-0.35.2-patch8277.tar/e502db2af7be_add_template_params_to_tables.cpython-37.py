# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/e502db2af7be_add_template_params_to_tables.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1299 bytes
__doc__ = 'add template_params to tables\n\nRevision ID: e502db2af7be\nRevises: 5ccf602336a0\nCreate Date: 2018-05-09 23:45:14.296283\n\n'
revision = 'e502db2af7be'
down_revision = '5ccf602336a0'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('template_params', (sa.Text()), nullable=True))


def downgrade():
    try:
        op.drop_column('tables', 'template_params')
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e