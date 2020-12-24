# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/65903709c321_allow_dml.py
# Compiled at: 2018-08-15 11:21:52
"""allow_dml

Revision ID: 65903709c321
Revises: 4500485bde7d
Create Date: 2016-09-15 08:48:27.284752

"""
import logging
revision = '65903709c321'
down_revision = '4500485bde7d'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('dbs', sa.Column('allow_dml', sa.Boolean(), nullable=True))


def downgrade():
    try:
        op.drop_column('dbs', 'allow_dml')
    except Exception as e:
        logging.exception(e)