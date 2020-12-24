# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/c611f2b591b8_dim_spec.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1216 bytes
__doc__ = 'dim_spec\n\nRevision ID: c611f2b591b8\nRevises: ad4d656d92bc\nCreate Date: 2016-11-02 17:36:04.970448\n\n'
revision = 'c611f2b591b8'
down_revision = 'ad4d656d92bc'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('columns', sa.Column('dimension_spec_json', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('columns', 'dimension_spec_json')