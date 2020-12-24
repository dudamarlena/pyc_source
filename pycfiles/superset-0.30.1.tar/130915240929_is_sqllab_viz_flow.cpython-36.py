# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/130915240929_is_sqllab_viz_flow.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1949 bytes
"""is_sqllab_view

Revision ID: 130915240929
Revises: f231d82b9b26
Create Date: 2018-04-03 08:19:34.098789

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '130915240929'
down_revision = 'f231d82b9b26'
Base = declarative_base()

class Table(Base):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'tables'
    id = sa.Column((sa.Integer), primary_key=True)
    sql = sa.Column(sa.Text)
    is_sqllab_view = sa.Column(sa.Boolean())


def upgrade():
    bind = op.get_bind()
    op.add_column('tables', sa.Column('is_sqllab_view',
      (sa.Boolean()),
      nullable=True,
      default=False,
      server_default=(sa.false())))
    session = db.Session(bind=bind)
    for tbl in session.query(Table).all():
        if tbl.sql:
            tbl.is_sqllab_view = True

    session.commit()
    db.session.close()


def downgrade():
    op.drop_column('tables', 'is_sqllab_view')