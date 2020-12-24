# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/alembic/versions/184f1bbcb916_language_und.py
# Compiled at: 2017-07-26 05:14:06
"""language_und

Revision ID: 184f1bbcb916
Revises: 6dfc3e2324aa
Create Date: 2017-07-25 16:38:39.439673

"""
revision = '184f1bbcb916'
down_revision = '6dfc3e2324aa'
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.orm import Session
language_table = table('language', column('id', sa.String), column('name', sa.String))

def upgrade():
    op.bulk_insert(language_table, [{'id': 'und', 'name': 'Undetermined'}])


def downgrade():
    connection = op.get_bind()
    session = Session(bind=connection)
    connection.execute(language_table.delete().where(language_table.c.id == 'und'))
    session.flush()