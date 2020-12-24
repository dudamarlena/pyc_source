# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/e004f76e951a_add_missing_not_null.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Add missing not null\n\nRevision ID: e004f76e951a\nRevises: ee25d267bf46\nCreate Date: 2016-10-06 15:28:17.418830\n'
from alembic import op, context
revision = 'e004f76e951a'
down_revision = 'ee25d267bf46'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.alter_column('layer_wmts', 'url', nullable=False, schema=schema)
    op.alter_column('layer_wmts', 'layer', nullable=False, schema=schema)
    op.execute(("UPDATE ONLY {schema}.layer_wmts SET image_type = 'image/png' where image_type IS NULL").format(schema=schema))
    op.alter_column('layer_wmts', 'image_type', nullable=False, schema=schema)
    op.alter_column('layer_wms', 'ogc_server_id', nullable=False, schema=schema)
    op.alter_column('layer_wms', 'layer', nullable=False, schema=schema)
    op.execute(("UPDATE ONLY {schema}.layer_wms SET time_mode = 'disabled' where time_mode IS NULL").format(schema=schema))
    op.alter_column('layer_wms', 'time_mode', nullable=False, schema=schema)
    op.execute(("UPDATE ONLY {schema}.layer_wms SET time_widget = 'slider' where time_widget IS NULL").format(schema=schema))
    op.alter_column('layer_wms', 'time_widget', nullable=False, schema=schema)
    op.execute(("UPDATE ONLY {schema}.ogc_server SET image_type = 'image/png' where image_type IS NULL").format(schema=schema))
    op.alter_column('ogc_server', 'image_type', nullable=False, schema=schema)
    op.execute(("UPDATE ONLY {schema}.ogc_server SET type = 'mapserver' where type IS NULL").format(schema=schema))
    op.alter_column('ogc_server', 'type', nullable=False, schema=schema)
    op.execute(("UPDATE ONLY {schema}.ogc_server SET auth = 'Standard auth' where auth IS NULL").format(schema=schema))
    op.alter_column('ogc_server', 'auth', nullable=False, schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.alter_column('layer_wmts', 'url', nullable=True, schema=schema)
    op.alter_column('layer_wmts', 'layer', nullable=True, schema=schema)
    op.alter_column('layer_wmts', 'image_type', nullable=True, schema=schema)
    op.alter_column('layer_wms', 'ogc_server_id', nullable=True, schema=schema)
    op.alter_column('layer_wms', 'layer', nullable=True, schema=schema)
    op.alter_column('layer_wms', 'time_mode', nullable=True, schema=schema)
    op.alter_column('layer_wms', 'time_widget', nullable=True, schema=schema)
    op.alter_column('ogc_server', 'image_type', nullable=True, schema=schema)
    op.alter_column('ogc_server', 'type', nullable=True, schema=schema)
    op.alter_column('ogc_server', 'auth', nullable=True, schema=schema)