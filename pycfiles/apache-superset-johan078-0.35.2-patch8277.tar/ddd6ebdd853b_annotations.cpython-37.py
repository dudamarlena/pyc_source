# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/ddd6ebdd853b_annotations.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2996 bytes
__doc__ = 'annotations\n\nRevision ID: ddd6ebdd853b\nRevises: ca69c70ec99b\nCreate Date: 2017-09-13 16:36:39.144489\n\n'
import sqlalchemy as sa
from alembic import op
revision = 'ddd6ebdd853b'
down_revision = 'ca69c70ec99b'

def upgrade():
    op.create_table('annotation_layer', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('name', sa.String(length=250), nullable=True), sa.Column('descr', (sa.Text()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_table('annotation', sa.Column('created_on', (sa.DateTime()), nullable=True), sa.Column('changed_on', (sa.DateTime()), nullable=True), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('start_dttm', (sa.DateTime()), nullable=True), sa.Column('end_dttm', (sa.DateTime()), nullable=True), sa.Column('layer_id', (sa.Integer()), nullable=True), sa.Column('short_descr', sa.String(length=500), nullable=True), sa.Column('long_descr', (sa.Text()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['layer_id'], ['annotation_layer.id']), sa.PrimaryKeyConstraint('id'))
    op.create_index('ti_dag_state',
      'annotation',
      [
     'layer_id', 'start_dttm', 'end_dttm'],
      unique=False)


def downgrade():
    op.drop_index('ti_dag_state', table_name='annotation')
    op.drop_table('annotation')
    op.drop_table('annotation_layer')