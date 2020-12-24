# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/20137477bd02_update_icons_url.py
# Compiled at: 2019-04-23 07:29:02
"""Update icons url

Revision ID: 20137477bd02
Revises: 415746eb9f6
Create Date: 2014-12-10 17:50:36.176587
"""
from alembic import op, context
revision = '20137477bd02'
down_revision = '1d5d4abfebd1'

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    updates = [
     "UPDATE %(schema)s.%(table)s SET %(column)s = 'static:///' || %(column)s WHERE (%(column)s IS NOT NULL) AND (NOT %(column)s = '') AND NOT (%(column)s LIKE 'http%%') AND NOT (%(column)s LIKE '/%%')",
     "UPDATE %(schema)s.%(table)s SET %(column)s = 'static://' || %(column)s WHERE (%(column)s IS NOT NULL) AND (NOT %(column)s = '') AND NOT (%(column)s LIKE 'http%%') AND NOT (%(column)s LIKE 'static://%%')"]
    for update in updates:
        op.execute(update % {'schema': schema, 
           'table': 'theme', 'column': 'icon'})
        op.execute(update % {'schema': schema, 
           'table': 'layerv1', 'column': 'icon'})
        op.execute(update % {'schema': schema, 
           'table': 'layerv1', 'column': 'kml'})
        op.execute(update % {'schema': schema, 
           'table': 'layerv1', 'column': 'legend_image'})


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    updates = [
     "UPDATE %(schema)s.%(table)s SET %(column)s = substring(%(column)s from 11) WHERE %(column)s LIKE 'static:///%%'",
     "UPDATE %(schema)s.%(table)s SET %(column)s = substring(%(column)s from 10) WHERE %(column)s LIKE 'static://%%'"]
    for update in updates:
        op.execute(update % {'schema': schema, 
           'table': 'theme', 'column': 'icon'})
        op.execute(update % {'schema': schema, 
           'table': 'layerv1', 'column': 'icon'})
        op.execute(update % {'schema': schema, 
           'table': 'layerv1', 'column': 'kml'})
        op.execute(update % {'schema': schema, 
           'table': 'layerv1', 'column': 'legend_image'})