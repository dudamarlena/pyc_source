# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/1a4d62b02630_199_sources.py
# Compiled at: 2017-06-22 05:19:07
"""199 Sources.

Revision ID: 1a4d62b02630
Revises: 2a38d364113b
Create Date: 2015-12-08 12:06:20.303601

"""
revision = '1a4d62b02630'
down_revision = '2a38d364113b'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('source', sa.Column('id', sa.Integer(), nullable=False), sa.Column('citation', sa.Text(), nullable=False), sa.PrimaryKeyConstraint('id'))
    op.create_table('conceptscheme_source', sa.Column('conceptscheme_id', sa.Integer(), nullable=False), sa.Column('source_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['conceptscheme_id'], ['conceptscheme.id']), sa.ForeignKeyConstraint(['source_id'], ['source.id']), sa.PrimaryKeyConstraint('conceptscheme_id', 'source_id'))
    op.create_table('concept_source', sa.Column('concept_id', sa.Integer(), nullable=False), sa.Column('source_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['concept_id'], ['concept.id']), sa.ForeignKeyConstraint(['source_id'], ['source.id']), sa.PrimaryKeyConstraint('concept_id', 'source_id'))


def downgrade():
    op.drop_table('conceptscheme_source')
    op.drop_table('concept_source')
    op.drop_table('source')