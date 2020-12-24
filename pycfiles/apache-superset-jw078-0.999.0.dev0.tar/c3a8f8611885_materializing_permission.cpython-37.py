# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/c3a8f8611885_materializing_permission.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2172 bytes
__doc__ = 'Materializing permission\n\nRevision ID: c3a8f8611885\nRevises: 4fa88fe24e94\nCreate Date: 2016-04-25 08:54:04.303859\n\n'
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = 'c3a8f8611885'
down_revision = '4fa88fe24e94'
Base = declarative_base()

class Slice(Base):
    """Slice"""
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    slice_name = Column(String(250))
    druid_datasource_id = Column(Integer, ForeignKey('datasources.id'))
    table_id = Column(Integer, ForeignKey('tables.id'))
    perm = Column(String(2000))


def upgrade():
    bind = op.get_bind()
    op.add_column('slices', sa.Column('perm', sa.String(length=2000), nullable=True))
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        if slc.datasource:
            slc.perm = slc.datasource.perm
            session.merge(slc)
            session.commit()

    db.session.close()


def downgrade():
    with op.batch_alter_table('slices') as (batch_op):
        batch_op.drop_column('perm')