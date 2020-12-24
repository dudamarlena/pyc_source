# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/3ac8aca026fd_note_markup.py
# Compiled at: 2017-06-22 05:19:07
"""note_markup

Revision ID: 3ac8aca026fd
Revises: 1ad2b6fbcf22
Create Date: 2015-08-17 10:46:02.444677

"""
revision = '3ac8aca026fd'
down_revision = '1ad2b6fbcf22'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('note', sa.Column('markup', sa.String(20)))


def downgrade():
    op.drop_column('note', 'markup')