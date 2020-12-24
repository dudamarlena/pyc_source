# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/a2d606a761d9_adding_favstar_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1561 bytes
__doc__ = 'adding favstar model\n\nRevision ID: a2d606a761d9\nRevises: 430039611635\nCreate Date: 2016-03-13 09:56:58.329512\n\n'
revision = 'a2d606a761d9'
down_revision = '18e88e1cc004'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('favstar', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('class_name', sa.String(length=50), nullable=True), sa.Column('obj_id', (sa.Integer()), nullable=True), sa.Column('dttm', (sa.DateTime()), nullable=True), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('favstar')