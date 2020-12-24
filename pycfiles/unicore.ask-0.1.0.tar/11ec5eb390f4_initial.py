# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.ask/unicore/ask/service/alembic/versions/11ec5eb390f4_initial.py
# Compiled at: 2015-03-13 10:41:44
"""initial

Revision ID: 11ec5eb390f4
Revises:
Create Date: 2015-03-12 16:08:13.250103

"""
revision = '11ec5eb390f4'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa, sqlalchemy_utils

def upgrade():
    op.create_table('questions', sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False), sa.Column('title', sa.Unicode(length=255), nullable=False), sa.Column('short_name', sa.Unicode(length=255), nullable=True), sa.Column('multiple', sa.Boolean(create_constraint=255), nullable=True), sa.Column('question_type', sa.Unicode(length=255), nullable=False), sa.PrimaryKeyConstraint('uuid'))
    op.create_table('question_options', sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False), sa.Column('title', sa.Unicode(length=255), nullable=True), sa.Column('short_name', sa.Unicode(length=255), nullable=True), sa.Column('question_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False), sa.ForeignKeyConstraint(['question_id'], ['questions.uuid']), sa.PrimaryKeyConstraint('uuid'))
    op.create_table('question_responses', sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False), sa.Column('text', sa.Unicode(length=255), nullable=False), sa.Column('question_option_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False), sa.ForeignKeyConstraint(['question_option_id'], ['question_options.uuid']), sa.PrimaryKeyConstraint('uuid'))


def downgrade():
    op.drop_table('question_responses')
    op.drop_table('question_options')
    op.drop_table('questions')