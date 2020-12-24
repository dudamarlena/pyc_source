# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/315b3f4da9b0_adding_log_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1543 bytes
__doc__ = 'adding log model\n\nRevision ID: 315b3f4da9b0\nRevises: 1a48a5411020\nCreate Date: 2015-12-04 11:16:58.226984\n\n'
revision = '315b3f4da9b0'
down_revision = '1a48a5411020'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('logs', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('action', sa.String(length=512), nullable=True), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('json', (sa.Text()), nullable=True), sa.Column('dttm', (sa.DateTime()), nullable=True), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('logs')