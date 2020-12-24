# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/116b9b79fc4d_internal_and_external_layer_tables_.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'internal and external layer tables refactoring, new ogc table\n\nRevision ID: 116b9b79fc4d\nRevises: 1418cb05921b\nCreate Date: 2015-10-28 12:21:59.162238\n'
from alembic import op, context
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Boolean, Unicode
revision = '116b9b79fc4d'
down_revision = 'a4f1aac9bda'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.create_table('server_ogc', Column('id', Integer, primary_key=True), Column('name', Unicode, nullable=False), Column('description', Unicode), Column('url', Unicode), Column('url_wfs', Unicode), Column('type', Unicode), Column('image_type', Unicode), Column('auth', Unicode), Column('wfs_support', Boolean, server_default='false'), Column('is_single_tile', Boolean, server_default='false'), schema=schema)
    op.create_table('layer_wms', Column('id', Integer, ForeignKey(schema + '.layer.id'), primary_key=True), Column('server_ogc_id', Integer, ForeignKey(schema + '.server_ogc.id')), Column('layer', Unicode), Column('style', Unicode), Column('time_mode', Unicode, server_default='disabled', nullable=False), Column('time_widget', Unicode, server_default='slider', nullable=False), schema=schema)
    op.execute("INSERT INTO %(schema)s.server_ogc (name, description, type, image_type,   auth, wfs_support) SELECT 'source for ' || image_type AS name,   'default source for internal ' || image_type AS description,   'mapserver' AS type,   image_type,   'Standard auth' AS auth,   'true' AS wfs_support FROM (  SELECT UNNEST(ARRAY['image/jpeg', 'image/png']) AS image_type) AS foo" % {'schema': schema})
    op.execute("INSERT INTO %(schema)s.server_ogc (name, description, type, image_type,   auth, wfs_support) SELECT 'source for ' || image_type AS name,   'default source for internal ' || image_type AS description,   'mapserver' AS type,   image_type,   'Standard auth' AS auth,   'true' AS wfs_support FROM (  SELECT DISTINCT(image_type) FROM %(schema)s.layer_internal_wms   WHERE image_type NOT IN ('image/jpeg', 'image/png')) as foo" % {'schema': schema})
    op.execute('INSERT INTO %(schema)s.layer_wms (id, server_ogc_id, layer, style,   time_mode, time_widget) SELECT lew.id, so.id, layer, style, time_mode, time_widget FROM %(schema)s.layer_internal_wms AS lew, %(schema)s.server_ogc AS so WHERE lew.image_type=so.image_type AND so.type IS NOT NULL' % {'schema': schema})
    op.execute("INSERT INTO %(schema)s.layer_wms (id, server_ogc_id, layer, style,   time_mode, time_widget) SELECT lew.id, so.id, layer, style, time_mode, time_widget FROM %(schema)s.layer_internal_wms AS lew, %(schema)s.server_ogc AS so WHERE lew.image_type IS NULL AND so.image_type='image/png'" % {'schema': schema})
    op.execute("INSERT INTO %(schema)s.server_ogc (name, url, type, image_type, auth, is_single_tile) SELECT 'source for ' || url, url, 'mapserver' AS type, image_type, 'none', CASE WHEN is_single_tile IS TRUE THEN TRUE ELSE FALSE END as is_single_tile FROM %(schema)s.layer_external_wms GROUP BY url, image_type, is_single_tile" % {'schema': schema})
    op.execute('INSERT INTO %(schema)s.layer_wms (id, server_ogc_id, layer, style,   time_mode, time_widget) SELECT lew.id, so.id, layer, style, time_mode, time_widget FROM %(schema)s.layer_external_wms as lew, %(schema)s.server_ogc as so WHERE lew.url=so.url AND lew.is_single_tile=so.is_single_tile AND lew.image_type=so.image_type' % {'schema': schema})
    op.drop_table('layer_external_wms', schema=schema)
    op.drop_table('layer_internal_wms', schema=schema)
    op.execute("UPDATE %(schema)s.treeitem SET type='l_wms' WHERE type='l_int_wms' OR type='l_ext_wms'" % {'schema': schema})


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.create_table('layer_internal_wms', Column('id', Integer, ForeignKey(schema + '.layer.id'), primary_key=True), Column('layer', Unicode), Column('image_type', Unicode(10)), Column('style', Unicode), Column('time_mode', Unicode(8)), Column('time_widget', Unicode(10), server_default='slider'), schema=schema)
    op.create_table('layer_external_wms', Column('id', Integer, ForeignKey(schema + '.layer.id'), primary_key=True), Column('url', Unicode), Column('layer', Unicode), Column('image_type', Unicode(10)), Column('style', Unicode), Column('is_single_tile', Boolean), Column('time_mode', Unicode(8)), Column('time_widget', Unicode(10), server_default='slider'), schema=schema)
    op.execute('INSERT INTO %(schema)s.layer_internal_wms (id, layer, image_type, style,   time_mode, time_widget) SELECT w.id, layer, image_type, style, time_mode, time_widget FROM %(schema)s.layer_wms AS w, %(schema)s.server_ogc AS o WHERE w.server_ogc_id=o.id AND o.type IS NOT NULL' % {'schema': schema})
    op.execute('INSERT INTO %(schema)s.layer_external_wms (id, url, layer, image_type, style,   is_single_tile, time_mode, time_widget) SELECT w.id, url, layer, image_type, style, is_single_tile, time_mode, time_widget FROM %(schema)s.layer_wms AS w, %(schema)s.server_ogc AS o WHERE w.server_ogc_id=o.id AND o.type IS NULL' % {'schema': schema})
    op.drop_table('layer_wms', schema=schema)
    op.drop_table('server_ogc', schema=schema)
    op.execute("UPDATE %(schema)s.treeitem SET type='l_int_wms' FROM %(schema)s.layer_internal_wms as w WHERE %(schema)s.treeitem.id=w.id" % {'schema': schema})
    op.execute("UPDATE %(schema)s.treeitem SET type='l_ext_wms' FROM %(schema)s.layer_external_wms as w WHERE %(schema)s.treeitem.id=w.id" % {'schema': schema})