# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/4451805bbaa1_remove_double_percents.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2843 bytes
"""remove double percents

Revision ID: 4451805bbaa1
Revises: afb7730f6a9c
Create Date: 2018-06-13 10:20:35.846744

"""
revision = '4451805bbaa1'
down_revision = 'bddc498dd179'
import json
from alembic import op
from sqlalchemy import Column, create_engine, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    datasource_id = Column(Integer, ForeignKey('tables.id'))
    datasource_type = Column(String(200))
    params = Column(Text)


class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    database_id = Column(Integer, ForeignKey('dbs.id'))


class Database(Base):
    __tablename__ = 'dbs'
    id = Column(Integer, primary_key=True)
    sqlalchemy_uri = Column(String(1024))


def replace(source, target):
    bind = op.get_bind()
    session = db.Session(bind=bind)
    query = session.query(Slice, Database).join(Table, Slice.datasource_id == Table.id).join(Database, Table.database_id == Database.id).filter(Slice.datasource_type == 'table').all()
    for slc, database in query:
        try:
            engine = create_engine(database.sqlalchemy_uri)
            if engine.dialect.identifier_preparer._double_percents:
                params = json.loads(slc.params)
                if 'adhoc_filters' in params:
                    for filt in params['adhoc_filters']:
                        if 'sqlExpression' in filt:
                            filt['sqlExpression'] = filt['sqlExpression'].replace(source, target)

                    slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def upgrade():
    replace('%%', '%')


def downgrade():
    replace('%', '%%')