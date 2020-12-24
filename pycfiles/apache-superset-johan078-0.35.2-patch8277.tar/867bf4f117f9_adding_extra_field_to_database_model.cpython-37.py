# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/867bf4f117f9_adding_extra_field_to_database_model.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1207 bytes
__doc__ = 'Adding extra field to Database model\n\nRevision ID: 867bf4f117f9\nRevises: fee7b758c130\nCreate Date: 2016-04-03 15:23:20.280841\n\n'
revision = '867bf4f117f9'
down_revision = 'fee7b758c130'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dbs', sa.Column('extra', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dbs', 'extra')