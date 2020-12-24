# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/e7e03dedade3_put_the_default_wms_server_in_the_.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Put the default WMS server in the servers part, add some constrains\n\nRevision ID: e7e03dedade3\nRevises: daf738d5bae4\nCreate Date: 2016-08-26 14:39:21.984921\n'
from alembic import op, context
revision = 'e7e03dedade3'
down_revision = '8117bb9bba16'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(('\n        UPDATE "{schema}".ogc_server\n        SET url = \'config://local/mapserv\'\n        WHERE url IS NULL\n    ').format(schema=schema))
    op.alter_column('ogc_server', 'url', nullable=False, schema=schema)
    op.create_unique_constraint('name_unique_ogc_server', 'ogc_server', ['name'], schema=schema)
    op.alter_column('treeitem', 'name', nullable=False, schema=schema)
    op.create_unique_constraint('type_name_unique_treeitem', 'treeitem', ['type', 'name'], schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.alter_column('ogc_server', 'url', nullable=True, schema=schema)
    op.drop_constraint('name_unique_ogc_server', 'ogc_server', schema=schema)
    op.alter_column('treeitem', 'name', nullable=True, schema=schema)
    op.drop_constraint('type_name_unique_treeitem', 'treeitem', schema=schema)
    op.execute(('\n        UPDATE "{schema}".ogc_server\n        SET url = NULL\n        WHERE url = \'config://local/mapserv\'\n    ').format(schema=schema))