# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/update/CONST_alembic/main/versions/d8ef99bc227e_be_able_to_delete_a_linked_functionality.py
# Compiled at: 2019-04-23 07:29:02
__doc__ = 'Be able to delete a linked functionality\n\nRevision ID: d8ef99bc227e\nRevises: 9268a1dffac0\nCreate Date: 2017-09-20 14:49:22.465328\n'
from alembic import op, context
import psycopg2
revision = 'd8ef99bc227e'
down_revision = '9268a1dffac0'
branch_labels = None
depends_on = None

def upgrade():
    schema = context.get_context().config.get_main_option('schema')
    for source, dest in [
     ('role_functionality', 'role'),
     ('role_functionality', 'functionality'),
     ('theme_functionality', 'theme'),
     ('theme_functionality', 'functionality')]:
        try:
            op.drop_constraint(('{}_{}_id_fkey').format(source, dest), source, schema=schema)
        except psycopg2.ProgrammingError as e:
            print e
            print "The constraint will probably don't exists, so we continue."

        op.create_foreign_key(('{}_{}_id_fkey').format(source, dest), source, source_schema=schema, local_cols=[('{}_id').format(dest)], referent_table=dest, referent_schema=schema, remote_cols=['id'], ondelete='cascade')


def downgrade():
    schema = context.get_context().config.get_main_option('schema')
    for source, dest in [
     ('role_functionality', 'role'),
     ('role_functionality', 'functionality'),
     ('theme_functionality', 'theme'),
     ('theme_functionality', 'functionality')]:
        op.drop_constraint(('{}_{}_id_fkey').format(source, dest), source, schema=schema)
        op.create_foreign_key(('{}_{}_id_fkey').format(source, dest), source, source_schema=schema, local_cols=[('{}_id').format(dest)], referent_table=dest, referent_schema=schema, remote_cols=['id'])