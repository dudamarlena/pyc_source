# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/d827694c7555_css_templates.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1780 bytes
__doc__ = 'css templates\n\nRevision ID: d827694c7555\nRevises: 43df8de3a5f4\nCreate Date: 2016-02-03 17:41:10.944019\n\n'
revision = 'd827694c7555'
down_revision = '43df8de3a5f4'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.create_table('css_templates', sa.Column('created_on', (sa.DateTime()), nullable=False), sa.Column('changed_on', (sa.DateTime()), nullable=False), sa.Column('id', (sa.Integer()), nullable=False), sa.Column('template_name', sa.String(length=250), nullable=True), sa.Column('css', (sa.Text()), nullable=True), sa.Column('changed_by_fk', (sa.Integer()), nullable=True), sa.Column('created_by_fk', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id']), sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('css_templates')