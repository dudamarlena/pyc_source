# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/130915240929_is_sqllab_viz_flow.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1949 bytes
__doc__ = 'is_sqllab_view\n\nRevision ID: 130915240929\nRevises: f231d82b9b26\nCreate Date: 2018-04-03 08:19:34.098789\n\n'
import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '130915240929'
down_revision = 'f231d82b9b26'
Base = declarative_base()

class Table(Base):
    """Table"""
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