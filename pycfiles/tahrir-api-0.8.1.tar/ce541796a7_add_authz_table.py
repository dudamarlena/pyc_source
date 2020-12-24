# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/ce541796a7_add_authz_table.py
# Compiled at: 2016-09-02 11:14:36
"""add authz table

Revision ID: ce541796a7
Revises: 4099fa344171
Create Date: 2013-12-13 15:30:16.576871

"""
revision = 'ce541796a7'
down_revision = '4099fa344171'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('authorizations', sa.Column('id', sa.Integer(), nullable=False), sa.Column('badge_id', sa.Unicode(length=128), nullable=False), sa.Column('person_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['badge_id'], ['badges.id']), sa.ForeignKeyConstraint(['person_id'], ['persons.id']), sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('authorizations')