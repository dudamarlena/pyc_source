# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/856955da8476_fix_sqlite_foreign_key.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4438 bytes
__doc__ = 'fix sqlite foreign key\n\nRevision ID: 856955da8476\nRevises: f23433877c24\nCreate Date: 2018-06-17 15:54:53.844230\n\n'
from alembic import op
import sqlalchemy as sa
revision = '856955da8476'
down_revision = 'f23433877c24'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    if conn.dialect.name == 'sqlite':
        chart_table = sa.Table('chart', sa.MetaData(), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('label', sa.String(length=200), nullable=True), sa.Column('conn_id', sa.String(length=250), nullable=False), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('chart_type', sa.String(length=100), nullable=True), sa.Column('sql_layout', sa.String(length=50), nullable=True), sa.Column('sql', (sa.Text()), nullable=True), sa.Column('y_log_scale', (sa.Boolean()), nullable=True), sa.Column('show_datatable', (sa.Boolean()), nullable=True), sa.Column('show_sql', (sa.Boolean()), nullable=True), sa.Column('height', (sa.Integer()), nullable=True), sa.Column('default_params', sa.String(length=5000), nullable=True), sa.Column('x_is_date', (sa.Boolean()), nullable=True), sa.Column('iteration_no', (sa.Integer()), nullable=True), sa.Column('last_modified', (sa.DateTime()), nullable=True), sa.PrimaryKeyConstraint('id'))
        with op.batch_alter_table('chart', copy_from=chart_table) as (batch_op):
            batch_op.create_foreign_key('chart_user_id_fkey', 'users', [
             'user_id'], ['id'])
        known_event_table = sa.Table('known_event', sa.MetaData(), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('label', sa.String(length=200), nullable=True), sa.Column('start_date', (sa.DateTime()), nullable=True), sa.Column('end_date', (sa.DateTime()), nullable=True), sa.Column('user_id', (sa.Integer()), nullable=True), sa.Column('known_event_type_id', (sa.Integer()), nullable=True), sa.Column('description', (sa.Text()), nullable=True), sa.ForeignKeyConstraint(['known_event_type_id'], [
         'known_event_type.id']), sa.PrimaryKeyConstraint('id'))
        with op.batch_alter_table('chart', copy_from=known_event_table) as (batch_op):
            batch_op.create_foreign_key('known_event_user_id_fkey', 'users', [
             'user_id'], ['id'])


def downgrade():
    pass