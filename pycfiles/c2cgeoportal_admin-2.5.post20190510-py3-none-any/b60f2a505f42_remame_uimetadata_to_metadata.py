# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/b60f2a505f42_remame_uimetadata_to_metadata.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Remame UIMetadata to Metadata\n\nRevision ID: b60f2a505f42\nRevises: daf738d5bae4\nCreate Date: 2016-08-26 15:13:59.102168\n'
from alembic import op, context
revision = 'b60f2a505f42'
down_revision = 'daf738d5bae4'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.rename_table('ui_metadata', 'metadata', schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.rename_table('metadata', 'ui_metadata', schema=schema)