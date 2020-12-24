# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/ad82a75afd82_add_query_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 3118 bytes
__doc__ = 'Update models to support storing the queries.\n\nRevision ID: ad82a75afd82\nRevises: f162a1dea4c4\nCreate Date: 2016-07-25 17:48:12.771103\n\n'
revision = 'ad82a75afd82'
down_revision = 'f162a1dea4c4'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('query', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('client_id', sa.String(length=11), nullable=False), sa.Column('database_id', (sa.Integer()), nullable=False), sa.Column('tmp_table_name', sa.String(length=256), nullable=True), sa.Column('tab_name', sa.String(length=256), nullable=True), sa.Column('sql_editor_id', sa.String(length=256), nullable=True), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('status', sa.String(length=16), nullable=True), sa.Column('name', sa.String(length=256), nullable=True), sa.Column('schema', sa.String(length=256), nullable=True), sa.Column('sql', (sa.Text()), nullable=True), sa.Column('select_sql', (sa.Text()), nullable=True), sa.Column('executed_sql', (sa.Text()), nullable=True), sa.Column('limit', (sa.Integer()), nullable=True), sa.Column('limit_used', (sa.Boolean()), nullable=True), sa.Column('select_as_cta', (sa.Boolean()), nullable=True), sa.Column('select_as_cta_used', (sa.Boolean()), nullable=True), sa.Column('progress', (sa.Integer()), nullable=True), sa.Column('rows', (sa.Integer()), nullable=True), sa.Column('error_message', (sa.Text()), nullable=True), sa.Column('start_time', sa.Numeric(precision=20, scale=6), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('end_time', sa.Numeric(precision=20, scale=6), nullable=True), sa.ForeignKeyConstraint(['database_id'], ['dbs.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))
    op.add_column('dbs', sa.Column('select_as_create_table_as', (sa.Boolean()), nullable=True))
    op.create_index((op.f('ti_user_id_changed_on')),
      'query', ['user_id', 'changed_on'], unique=False)


def downgrade():
    op.drop_table('query')
    op.drop_column('dbs', 'select_as_create_table_as')