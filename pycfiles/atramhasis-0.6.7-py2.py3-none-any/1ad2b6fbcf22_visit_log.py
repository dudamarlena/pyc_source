# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/1ad2b6fbcf22_visit_log.py
# Compiled at: 2017-06-22 05:19:07
"""visit_log

Revision ID: 1ad2b6fbcf22
Revises: 441c5a16ef8
Create Date: 2015-07-27 13:29:04.840631

"""
revision = '1ad2b6fbcf22'
down_revision = '441c5a16ef8'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('conceptscheme_visit_log', sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True), sa.Column('conceptscheme_id', sa.String(), nullable=False), sa.Column('visited_at', sa.DateTime(), nullable=False), sa.Column('origin', sa.String, nullable=False))
    op.create_table('concept_visit_log', sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True), sa.Column('concept_id', sa.Integer(), nullable=False), sa.Column('conceptscheme_id', sa.String(), nullable=False), sa.Column('visited_at', sa.DateTime(), nullable=False), sa.Column('origin', sa.String, nullable=False))


def downgrade():
    op.drop_table('concept_visit_log')
    op.drop_table('conceptscheme_visit_log')