# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sachowdh/code/fedora-infra/badges/tahrir-api/alembic/versions/3c7fd5b4e2c2_add_two_new_columns_.py
# Compiled at: 2016-04-21 17:38:50
"""Add two new columns for Person.

Revision ID: 3c7fd5b4e2c2
Revises: 24282792d72a
Create Date: 2013-06-26 14:46:28.361709

"""
revision = '3c7fd5b4e2c2'
down_revision = '16943d9088cf'
import tahrir_api
from alembic import op
import sqlalchemy as sa, datetime

def upgrade():
    op.add_column('persons', sa.Column('created_on', sa.DateTime()))
    op.add_column('persons', sa.Column('opt_out', sa.Boolean()))
    engine = op.get_bind().engine
    session_maker = sa.orm.sessionmaker(bind=engine)
    session = sa.orm.scoped_session(session_maker)
    persons = session.query(tahrir_api.model.Person).all()
    for person in persons:
        person.created_on = datetime.datetime.now()
        person.opt_out = False

    session.commit()


def downgrade():
    op.drop_column('persons', 'opt_out')
    op.drop_column('persons', 'created_on')