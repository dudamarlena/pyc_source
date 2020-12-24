# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/senan/projects/betanin/betanin_migrations/versions/6017dab0ffd9_.py
# Compiled at: 2019-08-10 08:47:23
# Size of source mod 2**32: 1423 bytes
"""empty message

Revision ID: 6017dab0ffd9
Revises: 
Create Date: 2019-07-12 17:06:44.486199

"""
from alembic import op
import sqlalchemy as sa
revision = '6017dab0ffd9'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('torrents', sa.Column('id', (sa.Integer()), nullable=False),
      sa.Column('name', (sa.String()), nullable=True),
      sa.Column('path', (sa.String()), nullable=True),
      sa.Column('status', sa.Enum('COMPLETED', 'ENQUEUED', 'FAILED', 'IGNORED', 'NEEDS_INPUT', 'PROCESSING', name='status'), nullable=True),
      sa.Column('created', (sa.DateTime()), nullable=True),
      sa.Column('updated', (sa.DateTime()), nullable=True),
      (sa.PrimaryKeyConstraint('id')),
      sqlite_autoincrement=True)
    op.create_table('lines', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('index', (sa.Integer()), nullable=True), sa.Column('data', (sa.String()), nullable=True), sa.Column('torrent_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['torrent_id'], ['torrents.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('lines')
    op.drop_table('torrents')