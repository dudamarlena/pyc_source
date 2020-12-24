# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/e502db2af7be_add_template_params_to_tables.py
# Compiled at: 2018-08-15 11:21:52
"""add template_params to tables

Revision ID: e502db2af7be
Revises: 5ccf602336a0
Create Date: 2018-05-09 23:45:14.296283

"""
revision = 'e502db2af7be'
down_revision = '5ccf602336a0'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('tables', sa.Column('template_params', sa.Text(), nullable=True))


def downgrade():
    try:
        op.drop_column('tables', 'template_params')
    except Exception as e:
        logging.warning(str(e))