# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/db0c65b146bd_update_slice_model_json.py
# Compiled at: 2018-08-15 11:21:52
"""update_slice_model_json

Revision ID: db0c65b146bd
Revises: f18570e03440
Create Date: 2017-01-24 12:31:06.541746

"""
revision = 'db0c65b146bd'
down_revision = 'f18570e03440'
from alembic import op
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from superset import db
from superset.legacy import cast_form_data
Base = declarative_base()

class Slice(Base):
    """Declarative class to do query in upgrade"""
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    datasource_type = Column(String(200))
    slice_name = Column(String(200))
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    slices = session.query(Slice).all()
    slice_len = len(slices)
    for i, slc in enumerate(slices):
        try:
            d = json.loads(slc.params or '{}')
            d = cast_form_data(d)
            slc.params = json.dumps(d, indent=2, sort_keys=True)
            session.merge(slc)
            session.commit()
            print ('Upgraded ({}/{}): {}').format(i, slice_len, slc.slice_name)
        except Exception as e:
            print slc.slice_name + ' error: ' + str(e)

    session.close()


def downgrade():
    pass