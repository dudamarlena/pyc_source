# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/d2ae31099d61_increase_text_size_for_mysql.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1546 bytes
"""Increase text size for MySQL (not relevant for other DBs' text types)

Revision ID: d2ae31099d61
Revises: 947454bf1dff
Create Date: 2017-08-18 17:07:16.686130

"""
from alembic import op
from sqlalchemy.dialects import mysql
from alembic import context
revision = 'd2ae31099d61'
down_revision = '947454bf1dff'
branch_labels = None
depends_on = None

def upgrade():
    if context.config.get_main_option('sqlalchemy.url').startswith('mysql'):
        op.alter_column(table_name='variable', column_name='val', type_=(mysql.MEDIUMTEXT))


def downgrade():
    if context.config.get_main_option('sqlalchemy.url').startswith('mysql'):
        op.alter_column(table_name='variable', column_name='val', type_=(mysql.TEXT))