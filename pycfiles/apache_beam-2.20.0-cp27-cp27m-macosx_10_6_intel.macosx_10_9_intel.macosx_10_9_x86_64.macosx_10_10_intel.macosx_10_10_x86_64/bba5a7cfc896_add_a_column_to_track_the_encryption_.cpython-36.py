# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bba5a7cfc896_add_a_column_to_track_the_encryption_.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1374 bytes
__doc__ = "Add a column to track the encryption state of the 'Extra' field in connection\n\nRevision ID: bba5a7cfc896\nRevises: bbc73705a13e\nCreate Date: 2016-01-29 15:10:32.656425\n\n"
from alembic import op
import sqlalchemy as sa
revision = 'bba5a7cfc896'
down_revision = 'bbc73705a13e'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('connection', sa.Column('is_extra_encrypted', (sa.Boolean), default=False))


def downgrade():
    op.drop_column('connection', 'is_extra_encrypted')