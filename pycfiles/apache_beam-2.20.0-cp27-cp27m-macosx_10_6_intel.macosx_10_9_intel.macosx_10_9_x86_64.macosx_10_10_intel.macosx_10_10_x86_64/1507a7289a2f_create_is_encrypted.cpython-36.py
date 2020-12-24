# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/1507a7289a2f_create_is_encrypted.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2203 bytes
__doc__ = 'create is_encrypted\n\nRevision ID: 1507a7289a2f\nRevises: e3a246e0dc1\nCreate Date: 2015-08-18 18:57:51.927315\n\n'
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