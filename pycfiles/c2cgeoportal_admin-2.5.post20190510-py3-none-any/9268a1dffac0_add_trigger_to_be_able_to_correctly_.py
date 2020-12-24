# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/9268a1dffac0_add_trigger_to_be_able_to_correctly_.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Add trigger to be able to correctly change the role name\n\nRevision ID: 9268a1dffac0\nRevises: 32b21aa1d0ed\nCreate Date: 2017-01-11 11:07:53.042003\n'
from alembic import op, context
revision = '9268a1dffac0'
down_revision = '32b21aa1d0ed'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(('\nCREATE OR REPLACE FUNCTION {schema}.on_role_name_change()\nRETURNS trigger AS\n$$\nBEGIN\nIF NEW.name <> OLD.name THEN\nUPDATE {schema}."user" SET role_name = NEW.name WHERE role_name = OLD.name;\nEND IF;\nRETURN NEW;\nEND;\n$$\nLANGUAGE plpgsql').format(schema=schema))
    op.execute(('CREATE TRIGGER on_role_name_change AFTER UPDATE ON {schema}.role FOR EACH ROW EXECUTE PROCEDURE {schema}.on_role_name_change()').format(schema=schema))


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    op.execute(('DROP TRIGGER on_role_name_change ON {schema}.role').format(schema=schema))
    op.execute(('DROP FUNCTION {schema}.on_role_name_change()').format(schema=schema))