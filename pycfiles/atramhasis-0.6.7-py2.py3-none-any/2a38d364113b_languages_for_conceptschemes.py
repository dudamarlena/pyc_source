# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/2a38d364113b_languages_for_conceptschemes.py
# Compiled at: 2017-06-22 05:19:07
"""Languages for conceptschemes.

Revision ID: 2a38d364113b
Revises: 3ac8aca026fd
Create Date: 2015-11-19 15:03:45.587093

"""
revision = '2a38d364113b'
down_revision = '3ac8aca026fd'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('conceptscheme_language', sa.Column('conceptscheme_id', sa.Integer(), nullable=False), sa.Column('language_id', sa.String(length=64), nullable=False), sa.ForeignKeyConstraint(['conceptscheme_id'], ['conceptscheme.id']), sa.ForeignKeyConstraint(['language_id'], ['language.id']), sa.PrimaryKeyConstraint('conceptscheme_id', 'language_id'))


def downgrade():
    op.drop_table('conceptscheme_language')