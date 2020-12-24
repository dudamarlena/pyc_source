# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/32527659d57b_move_exclude_properties_from_layerv1_to_.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Move exclude_properties from LayerV1 to Layer\n\nRevision ID: 32527659d57b\nRevises: 5109242131ce\nCreate Date: 2015-10-19 16:31:24.894791\n'
from alembic import op, context
from sqlalchemy import Column
from sqlalchemy.types import Unicode
revision = '32527659d57b'
down_revision = '5109242131ce'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('layer', Column('exclude_properties', Unicode), schema=schema)
    op.execute('UPDATE %(schema)s.layer as l1 SET exclude_properties = l2.exclude_properties FROM %(schema)s.layerv1 as l2 WHERE l1.id = l2.id' % {'schema': schema})
    op.drop_column('layerv1', 'exclude_properties', schema=schema)


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.add_column('layerv1', Column('exclude_properties', Unicode), schema=schema)
    op.execute('UPDATE %(schema)s.layerv1 as l1 SET exclude_properties = l2.exclude_properties FROM %(schema)s.layer as l2 WHERE l1.id = l2.id' % {'schema': schema})
    op.drop_column('layer', 'exclude_properties', schema=schema)