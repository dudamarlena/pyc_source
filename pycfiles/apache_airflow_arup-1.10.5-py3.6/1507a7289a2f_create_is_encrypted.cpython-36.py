# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/1507a7289a2f_create_is_encrypted.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2203 bytes
"""create is_encrypted

Revision ID: 1507a7289a2f
Revises: e3a246e0dc1
Create Date: 2015-08-18 18:57:51.927315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
revision = '1507a7289a2f'
down_revision = 'e3a246e0dc1'
branch_labels = None
depends_on = None
connectionhelper = sa.Table('connection', sa.MetaData(), sa.Column('id', (sa.Integer), primary_key=True), sa.Column('is_encrypted'))

def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    if 'connection' in inspector.get_table_names():
        col_names = [c['name'] for c in inspector.get_columns('connection')]
        if 'is_encrypted' in col_names:
            return
    op.add_column('connection', sa.Column('is_encrypted', (sa.Boolean), unique=False, default=False))
    conn = op.get_bind()
    conn.execute(connectionhelper.update().values(is_encrypted=False))


def downgrade():
    op.drop_column('connection', 'is_encrypted')