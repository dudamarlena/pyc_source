# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/5e4a03ef0bf0_add_request_access_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1846 bytes
__doc__ = 'Add access_request table to manage requests to access datastores.\n\nRevision ID: 5e4a03ef0bf0\nRevises: 41f6a59a61f2\nCreate Date: 2016-09-09 17:39:57.846309\n\n'
import sqlalchemy as sa
from alembic import op
revision = '5e4a03ef0bf0'
down_revision = 'b347b202819b'

def upgrade():
    op.create_table('access_request', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('datasource_type', sa.String(length=200), nullable=True), sa.Column('datasource_id', (sa.Integer()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('access_request')