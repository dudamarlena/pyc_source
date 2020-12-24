# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/596ba21e3833_separate_local_internal.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'separate local internal\n\nRevision ID: 596ba21e3833\nRevises: ec82a8906649\nCreate Date: 2016-09-08 16:49:58.865617\n'
from alembic import op, context
revision = '596ba21e3833'
down_revision = 'ec82a8906649'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(('\n        UPDATE "{schema}".ogc_server\n        SET url = \'config://internal/mapserv\'\n        WHERE url = \'config://local/mapserv\'\n    ').format(schema=schema))


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(('\n        UPDATE "{schema}".ogc_server\n        SET url = \'config://local/mapserv\'\n        WHERE url = \'config://internal/mapserv\'\n    ').format(schema=schema))