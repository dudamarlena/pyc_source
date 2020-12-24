# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/meatpuppet/dev/lspace/lspace/migrations/versions/b9f9b5b4e882_.py
# Compiled at: 2019-06-16 09:31:16
# Size of source mod 2**32: 1234 bytes
"""empty message

Revision ID: b9f9b5b4e882
Revises: 91732d5540b9
Create Date: 2019-06-14 10:39:42.779170

"""
from alembic import op
import sqlalchemy as sa
revision = 'b9f9b5b4e882'
down_revision = '91732d5540b9'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('shelves', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('name', sa.String(length=100), nullable=True), sa.PrimaryKeyConstraint('id', name=(op.f('pk_shelves'))))
    with op.batch_alter_table('books', schema=None) as (batch_op):
        batch_op.add_column(sa.Column('shelve_id', (sa.Integer()), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_books_shelve_id_shelves'), 'shelves', ['shelve_id'], ['id'])


def downgrade():
    with op.batch_alter_table('books', schema=None) as (batch_op):
        batch_op.drop_constraint((batch_op.f('fk_books_shelve_id_shelves')), type_='foreignkey')
        batch_op.drop_column('shelve_id')
    op.drop_table('shelves')