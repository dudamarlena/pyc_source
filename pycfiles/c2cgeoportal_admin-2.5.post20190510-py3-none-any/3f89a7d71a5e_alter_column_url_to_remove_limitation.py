# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/static/versions/3f89a7d71a5e_alter_column_url_to_remove_limitation.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Alter_column_url_to_remove_limitation\n\nRevision ID: 3f89a7d71a5e\nRevises:\nCreate Date: 2014-12-18 10:27:52.263992\n'
from alembic import op, context
from sqlalchemy import types
revision = '3f89a7d71a5e'
down_revision = None

def upgrade():
    schema = ('{0!s}_static').format(context.get_context().config.get_main_option('schema'))
    op.alter_column('shorturl', 'url', type_=types.Unicode, schema=schema)


def downgrade():
    pass