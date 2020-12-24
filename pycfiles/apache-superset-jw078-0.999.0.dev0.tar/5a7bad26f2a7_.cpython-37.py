# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/5a7bad26f2a7_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1327 bytes
__doc__ = 'empty message\n\nRevision ID: 5a7bad26f2a7\nRevises: 4e6a06bad7a8\nCreate Date: 2015-10-05 10:32:15.850753\n\n'
revision = '5a7bad26f2a7'
down_revision = '4e6a06bad7a8'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dashboards', sa.Column('css', (sa.Text()), nullable=True))
    op.add_column('dashboards', sa.Column('description', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dashboards', 'description')
    op.drop_column('dashboards', 'css')