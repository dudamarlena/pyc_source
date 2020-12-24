# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1a48a5411020_adding_slug_to_dash.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1385 bytes
__doc__ = 'adding slug to dash\n\nRevision ID: 1a48a5411020\nRevises: 289ce07647b\nCreate Date: 2015-12-04 09:42:16.973264\n\n'
revision = '1a48a5411020'
down_revision = '289ce07647b'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dashboards', sa.Column('slug', sa.String(length=255), nullable=True))
    try:
        op.create_unique_constraint('idx_unique_slug', 'dashboards', ['slug'])
    except:
        pass


def downgrade():
    op.drop_constraint(None, 'dashboards', type_='unique')
    op.drop_column('dashboards', 'slug')