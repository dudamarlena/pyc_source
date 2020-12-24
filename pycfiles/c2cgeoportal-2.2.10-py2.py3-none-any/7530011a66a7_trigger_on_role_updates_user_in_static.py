# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/7530011a66a7_trigger_on_role_updates_user_in_static.py
# Compiled at: 2019-04-23 07:29:02
"""trigger_on_role_updates_user_in_static

Revision ID: 7530011a66a7
Revises: d8ef99bc227e
Create Date: 2018-03-23 09:08:56.910629
"""
from alembic import op, context
revision = '7530011a66a7'
down_revision = 'd8ef99bc227e'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    staticschema = schema + '_static'
    op.execute(('\nCREATE OR REPLACE FUNCTION {schema}.on_role_name_change()\nRETURNS trigger AS\n$$\nBEGIN\nIF NEW.name <> OLD.name THEN\nUPDATE {staticschema}."user" SET role_name = NEW.name WHERE role_name = OLD.name;\nEND IF;\nRETURN NEW;\nEND;\n$$\nLANGUAGE plpgsql').format(schema=schema, staticschema=staticschema))


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(('\nCREATE OR REPLACE FUNCTION {schema}.on_role_name_change()\nRETURNS trigger AS\n$$\nBEGIN\nIF NEW.name <> OLD.name THEN\nUPDATE {schema}."user" SET role_name = NEW.name WHERE role_name = OLD.name;\nEND IF;\nRETURN NEW;\nEND;\n$$\nLANGUAGE plpgsql').format(schema=schema))