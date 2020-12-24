# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/3b626e2a6783_sync_db_with_models.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4577 bytes
__doc__ = "Sync DB with the models.py.\n\nSqlite doesn't support alter on tables, that's why most of the operations\nare surrounded with try except.\n\nRevision ID: 3b626e2a6783\nRevises: 5e4a03ef0bf0\nCreate Date: 2016-09-22 10:21:33.618976\n\n"
import logging, sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql
from superset import db
from superset.utils.core import generic_find_constraint_name
revision = '3b626e2a6783'
down_revision = 'eca4694defa7'

def upgrade():
    try:
        slices_ibfk_1 = generic_find_constraint_name(table='slices',
          columns={
         'druid_datasource_id'},
          referenced='datasources',
          db=db)
        slices_ibfk_2 = generic_find_constraint_name(table='slices',
          columns={'table_id'},
          referenced='tables',
          db=db)
        with op.batch_alter_table('slices') as (batch_op):
            if slices_ibfk_1:
                batch_op.drop_constraint(slices_ibfk_1, type_='foreignkey')
            if slices_ibfk_2:
                batch_op.drop_constraint(slices_ibfk_2, type_='foreignkey')
            batch_op.drop_column('druid_datasource_id')
            batch_op.drop_column('table_id')
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e

    try:
        with op.batch_alter_table('columns') as (batch_op):
            batch_op.create_foreign_key(None, 'datasources', ['datasource_name'], ['datasource_name'])
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e

    try:
        with op.batch_alter_table('query') as (batch_op):
            batch_op.create_unique_constraint('client_id', ['client_id'])
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e

    try:
        with op.batch_alter_table('query') as (batch_op):
            batch_op.drop_column('name')
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e


def downgrade():
    try:
        with op.batch_alter_table('tables') as (batch_op):
            batch_op.create_index('table_name', ['table_name'], unique=True)
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e

    try:
        with op.batch_alter_table('slices') as (batch_op):
            batch_op.add_column(sa.Column('table_id',
              mysql.INTEGER(display_width=11),
              autoincrement=False,
              nullable=True))
            batch_op.add_column(sa.Column('druid_datasource_id',
              (sa.Integer()),
              autoincrement=False,
              nullable=True))
            batch_op.create_foreign_key('slices_ibfk_1', 'datasources', ['druid_datasource_id'], ['id'])
            batch_op.create_foreign_key('slices_ibfk_2', 'tables', ['table_id'], ['id'])
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e

    try:
        fk_columns = generic_find_constraint_name(table='columns',
          columns={
         'datasource_name'},
          referenced='datasources',
          db=db)
        with op.batch_alter_table('columns') as (batch_op):
            batch_op.drop_constraint(fk_columns, type_='foreignkey')
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e

    op.add_column('query', sa.Column('name', sa.String(length=256), nullable=True))
    try:
        with op.batch_alter_table('query') as (batch_op):
            batch_op.drop_constraint('client_id', type_='unique')
    except Exception as e:
        try:
            logging.warning(str(e))
        finally:
            e = None
            del e