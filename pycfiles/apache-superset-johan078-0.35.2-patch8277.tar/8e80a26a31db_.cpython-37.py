# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/8e80a26a31db_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1685 bytes
__doc__ = 'empty message\n\nRevision ID: 8e80a26a31db\nRevises: 2591d77e9831\nCreate Date: 2016-01-13 20:24:45.256437\n\n'
revision = '8e80a26a31db'
down_revision = '2591d77e9831'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('url', sa.Column('created_on', (sa.DateTime()), nullable=False), sa.Column('changed_on', (sa.DateTime()), nullable=False), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('url', (sa.Text()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('url')