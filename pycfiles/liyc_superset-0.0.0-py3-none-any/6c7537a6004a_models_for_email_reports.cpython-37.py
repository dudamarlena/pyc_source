# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\6c7537a6004a_models_for_email_reports.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 4501 bytes
"""models for email reports

Revision ID: 6c7537a6004a
Revises: e502db2af7be
Create Date: 2018-05-15 20:28:51.977572

"""
revision = '6c7537a6004a'
down_revision = 'a61b40f9f57f'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('dashboard_email_schedules', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('active', (sa.Boolean()), nullable=True), sa.Column('crontab', sa.String(length=50), nullable=True), sa.Column('recipients', (sa.Text()), nullable=True), sa.Column('deliver_as_group', (sa.Boolean()), nullable=True), sa.Column('delivery_type',
      sa.Enum('attachment', 'inline', name='emaildeliverytype'),
      nullable=True), sa.Column('dashboard_id', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('user_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['dashboard_id'], ['dashboards.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_index((op.f('ix_dashboard_email_schedules_active')),
      'dashboard_email_schedules',
      [
     'active'],
      unique=False)
    op.create_table('slice_email_schedules', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('active', (sa.Boolean()), nullable=True), sa.Column('crontab', sa.String(length=50), nullable=True), sa.Column('recipients', (sa.Text()), nullable=True), sa.Column('deliver_as_group', (sa.Boolean()), nullable=True), sa.Column('delivery_type',
      sa.Enum('attachment', 'inline', name='emaildeliverytype'),
      nullable=True), sa.Column('slice_id', (sa.Integer()), nullable=True), sa.Column('email_format',
      sa.Enum('visualization', 'data', name='sliceemailreportformat'),
      nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('user_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['slice_id'], ['slices.id']), sa.ForeignKeyConstraint(['user_id'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_index((op.f('ix_slice_email_schedules_active')),
      'slice_email_schedules',
      [
     'active'],
      unique=False)


def downgrade():
    op.drop_index((op.f('ix_slice_email_schedules_active')),
      table_name='slice_email_schedules')
    op.drop_table('slice_email_schedules')
    op.drop_index((op.f('ix_dashboard_email_schedules_active')),
      table_name='dashboard_email_schedules')
    op.drop_table('dashboard_email_schedules')