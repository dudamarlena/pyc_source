# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/130915240929_is_sqllab_viz_flow.py
# Compiled at: 2018-08-15 11:21:52
"""is_sqllab_view

Revision ID: 130915240929
Revises: f231d82b9b26
Create Date: 2018-04-03 08:19:34.098789

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '130915240929'
down_revision = 'f231d82b9b26'
Base = declarative_base()

class Table(Base):
    """Declarative class to do query in upgrade"""
    __tablename__ = 'tables'
    id = sa.Column(sa.Integer, primary_key=True)
    sql = sa.Column(sa.Text)
    is_sqllab_view = sa.Column(sa.Boolean())


def upgrade():
    bind = op.get_bind()
    op.add_column('tables', sa.Column('is_sqllab_view', sa.Boolean(), nullable=True, default=False, server_default=sa.false()))
    session = db.Session(bind=bind)
    for tbl in session.query(Table).all():
        if tbl.sql:
            tbl.is_sqllab_view = True

    session.commit()
    db.session.close()


def downgrade():
    op.drop_column('tables', 'is_sqllab_view')