# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/a65458420354_add_result_backend_time_logging.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1311 bytes
__doc__ = 'add_result_backend_time_logging\n\nRevision ID: a65458420354\nRevises: 2fcdcb35e487\nCreate Date: 2017-04-25 10:00:58.053120\n\n'
import sqlalchemy as sa
from alembic import op
revision = 'a65458420354'
down_revision = '2fcdcb35e487'

def upgrade():
    op.add_column('query', sa.Column('end_result_backend_time',
      sa.Numeric(precision=20, scale=6), nullable=True))


def downgrade():
    op.drop_column('query', 'end_result_backend_time')