# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/2879ed5a6297_issued_for.py
# Compiled at: 2016-04-21 17:38:50
"""issued_for

Revision ID: 2879ed5a6297
Revises: ce541796a7
Create Date: 2014-03-04 11:04:31.024949

"""
revision = '2879ed5a6297'
down_revision = 'ce541796a7'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('assertions', sa.Column('issued_for', sa.Unicode(256)))


def downgrade():
    op.drop_column('assertions', 'issued_for')