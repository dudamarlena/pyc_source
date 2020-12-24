# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/db527d8c4c78_add_db_verbose_name.py
# Compiled at: 2018-08-15 11:21:52
"""Add verbose name to DruidCluster and Database

Revision ID: db527d8c4c78
Revises: b318dfe5fb6c
Create Date: 2017-03-16 18:10:57.193035

"""
revision = 'db527d8c4c78'
down_revision = 'b318dfe5fb6c'
from alembic import op
import logging, sqlalchemy as sa

def upgrade():
    op.add_column('clusters', sa.Column('verbose_name', sa.String(length=250), nullable=True))
    op.add_column('dbs', sa.Column('verbose_name', sa.String(length=250), nullable=True))
    try:
        op.create_unique_constraint(None, 'dbs', ['verbose_name'])
        op.create_unique_constraint(None, 'clusters', ['verbose_name'])
    except Exception as e:
        logging.info('Constraint not created, expected when using sqlite')

    return


def downgrade():
    try:
        op.drop_column('dbs', 'verbose_name')
        op.drop_column('clusters', 'verbose_name')
    except Exception as e:
        logging.exception(e)