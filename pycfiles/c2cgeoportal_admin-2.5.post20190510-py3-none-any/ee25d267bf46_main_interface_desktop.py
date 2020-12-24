# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/ee25d267bf46_main_interface_desktop.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'main interface => desktop\n\nRevision ID: ee25d267bf46\nRevises: 596ba21e3833\nCreate Date: 2016-09-21 11:39:37.086066\n'
from alembic import op, context
revision = 'ee25d267bf46'
down_revision = '596ba21e3833'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(("UPDATE ONLY {schema}.interface AS i SET name = 'desktop' where name = 'main'").format(schema=schema))


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(("UPDATE ONLY {schema}.interface AS i SET name = 'main' where name = 'desktop'").format(schema=schema))