# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.ask/unicore/ask/service/alembic/versions/2a4397511296_add_response_count_field.py
# Compiled at: 2015-03-13 10:41:44
"""add response count field

Revision ID: 2a4397511296
Revises: 11ec5eb390f4
Create Date: 2015-03-12 17:15:03.910473

"""
revision = '2a4397511296'
down_revision = '11ec5eb390f4'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('question_options', sa.Column('responses_count', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('question_options', 'responses_count')