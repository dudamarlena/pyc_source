# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/4fa88fe24e94_owners_many_to_many.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1940 bytes
__doc__ = 'owners_many_to_many\n\nRevision ID: 4fa88fe24e94\nRevises: b4456560d4f3\nCreate Date: 2016-04-15 17:58:33.842012\n\n'
revision = '4fa88fe24e94'
down_revision = 'b4456560d4f3'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('dashboard_user', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('dashboard_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['dashboard_id'], ['dashboards.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_table('slice_user', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('slice_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['slice_id'], ['slices.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('slice_user')
    op.drop_table('dashboard_user')