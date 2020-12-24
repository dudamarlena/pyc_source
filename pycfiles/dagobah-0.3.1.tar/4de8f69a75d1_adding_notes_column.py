# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /repos/dagobah/dagobah/backend/migrations/versions/4de8f69a75d1_adding_notes_column.py
# Compiled at: 2014-05-15 11:25:03
"""adding notes column

Revision ID: 4de8f69a75d1
Revises: 2ab7af991b87
Create Date: 2013-10-29 15:43:13.132113

"""
revision = '4de8f69a75d1'
down_revision = '2ab7af991b87'
from alembic import op
import sqlalchemy as sa

def upgrade():
    conn = op.get_bind()
    columns = conn.execute('select * from dagobah_job limit 1')._metadata.keys
    if 'notes' not in columns:
        op.add_column('dagobah_job', sa.Column('notes', sa.String(1000)))


def downgrade():
    op.drop_column('dagobah_job', 'notes')