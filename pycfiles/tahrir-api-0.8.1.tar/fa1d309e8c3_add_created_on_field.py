# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/fa1d309e8c3_add_created_on_field.py
# Compiled at: 2016-04-21 17:38:50
"""Add created_on field to issuers table.

Revision ID: fa1d309e8c3
Revises: 420c02357a1b
Create Date: 2013-06-10 12:30:31.850641

"""
revision = 'fa1d309e8c3'
down_revision = '420c02357a1b'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('issuers', sa.Column('created_on', sa.DateTime, nullable=False))


def downgrade():
    op.drop_column('issuers', 'created_on')