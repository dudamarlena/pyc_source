# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/meatpuppet/dev/lspace/lspace/migrations/versions/b142d6d9e8da_.py
# Compiled at: 2019-06-14 04:37:11
# Size of source mod 2**32: 1630 bytes
"""empty message

Revision ID: b142d6d9e8da
Revises: 
Create Date: 2019-05-11 14:42:35.971140

"""
from alembic import op
import sqlalchemy as sa
revision = 'b142d6d9e8da'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('authors', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('name', sa.String(length=100), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_table('books', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('title', sa.String(length=100), nullable=True), sa.Column('isbn13', sa.String(length=13), nullable=True), sa.Column('publisher', sa.String(length=100), nullable=True), sa.Column('year', (sa.Integer()), nullable=True), sa.Column('language', sa.String(length=20), nullable=True), sa.Column('md5sum', sa.String(length=32), nullable=True), sa.Column('path', sa.String(length=400), nullable=True), sa.PrimaryKeyConstraint('id'))
    op.create_table('book_author_association', sa.Column('book_id', (sa.Integer()), nullable=True), sa.Column('author_id', (sa.Integer()), nullable=True), sa.ForeignKeyConstraint(['author_id'], ['authors.id']), sa.ForeignKeyConstraint(['book_id'], ['books.id']))


def downgrade():
    op.drop_table('book_author_association')
    op.drop_table('books')
    op.drop_table('authors')