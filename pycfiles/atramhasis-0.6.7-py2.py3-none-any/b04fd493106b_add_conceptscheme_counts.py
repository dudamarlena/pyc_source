# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/b04fd493106b_add_conceptscheme_counts.py
# Compiled at: 2017-07-25 03:38:05
"""Add conceptscheme counts

Revision ID: b04fd493106b
Revises: 3bcf11802900
Create Date: 2016-11-02 07:36:17.940810

"""
revision = 'b04fd493106b'
down_revision = '3bcf11802900'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('conceptscheme_counts', sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True), sa.Column('conceptscheme_id', sa.String(), nullable=False), sa.Column('counted_at', sa.DateTime(), nullable=False), sa.Column('triples', sa.Integer, nullable=False), sa.Column('conceptscheme_triples', sa.Integer, nullable=False), sa.Column('avg_concept_triples', sa.Integer, nullable=False))


def downgrade():
    op.drop_table('conceptscheme_counts')