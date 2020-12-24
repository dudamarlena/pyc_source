# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1226819ee0e3_fix_wrong_constraint_on_table_columns.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2520 bytes
__doc__ = 'Fix wrong constraint on table columns\n\nRevision ID: 1226819ee0e3\nRevises: 956a063c52b3\nCreate Date: 2016-05-27 15:03:32.980343\n\n'
import logging
from alembic import op
from superset import db
from superset.utils.core import generic_find_constraint_name
revision = '1226819ee0e3'
down_revision = '956a063c52b3'
naming_convention = {'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'}

def find_constraint_name(upgrade=True):
    cols = {'column_name'} if upgrade else {'datasource_name'}
    return generic_find_constraint_name(table='columns',
      columns=cols,
      referenced='datasources',
      db=db)


def upgrade():
    try:
        constraint = find_constraint_name()
        with op.batch_alter_table('columns',
          naming_convention=naming_convention) as (batch_op):
            if constraint:
                batch_op.drop_constraint(constraint, type_='foreignkey')
            batch_op.create_foreign_key('fk_columns_datasource_name_datasources', 'datasources', [
             'datasource_name'], [
             'datasource_name'])
    except:
        logging.warning('Could not find or drop constraint on `columns`')


def downgrade():
    constraint = find_constraint_name(False) or 
    with op.batch_alter_table('columns',
      naming_convention=naming_convention) as (batch_op):
        batch_op.drop_constraint(constraint, type_='foreignkey')
        batch_op.create_foreign_key('fk_columns_column_name_datasources', 'datasources', [
         'column_name'], [
         'datasource_name'])