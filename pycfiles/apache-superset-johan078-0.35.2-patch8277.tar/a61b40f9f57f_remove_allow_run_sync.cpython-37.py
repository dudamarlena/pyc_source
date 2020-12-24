# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/a61b40f9f57f_remove_allow_run_sync.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1384 bytes
__doc__ = 'remove allow_run_sync\n\nRevision ID: a61b40f9f57f\nRevises: 46f444d8b9b7\nCreate Date: 2018-11-27 11:53:17.512627\n\n'
import sqlalchemy as sa
from alembic import op
revision = 'a61b40f9f57f'
down_revision = '46f444d8b9b7'

def upgrade():
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.drop_column('allow_run_sync')


def downgrade():
    op.add_column('dbs', sa.Column('allow_run_sync',
      sa.Integer(display_width=1),
      autoincrement=False,
      nullable=True))