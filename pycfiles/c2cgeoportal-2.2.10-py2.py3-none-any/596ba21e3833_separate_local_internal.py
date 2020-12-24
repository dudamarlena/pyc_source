# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/596ba21e3833_separate_local_internal.py
# Compiled at: 2019-04-23 07:29:02
"""separate local internal

Revision ID: 596ba21e3833
Revises: ec82a8906649
Create Date: 2016-09-08 16:49:58.865617
"""
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