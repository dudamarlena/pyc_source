# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/2fcdcb35e487_saved_queries.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2112 bytes
__doc__ = 'saved_queries\n\nRevision ID: 2fcdcb35e487\nRevises: a6c18f869a4e\nCreate Date: 2017-03-29 15:04:35.734190\n\n'
import sqlalchemy as sa
from alembic import op
revision = '2fcdcb35e487'
down_revision = 'a6c18f869a4e'

def upgrade():
    op.create_table('saved_query', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('db_id', (sa.Integer()), nullable=True), sa.Column('label', (sa.String(256)), nullable=True), sa.Column('schema', (sa.String(128)), nullable=True), sa.Column('sql', (sa.Text()), nullable=True), sa.Column('description', (sa.Text()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.ForeignKeyConstraint(['db_id'], ['dbs.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('saved_query')