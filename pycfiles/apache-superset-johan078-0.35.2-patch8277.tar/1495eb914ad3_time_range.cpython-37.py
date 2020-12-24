# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1495eb914ad3_time_range.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2561 bytes
__doc__ = 'time range\n\nRevision ID: 1495eb914ad3\nRevises: 258b5280a45e\nCreate Date: 2019-10-10 13:52:54.544475\n\n'
import json, logging
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
from superset.legacy import update_time_range
revision = '1495eb914ad3'
down_revision = '258b5280a45e'
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            form_data = json.loads(slc.params)
            update_time_range(form_data)
            slc.params = json.dumps(form_data, sort_keys=True)
        except Exception as ex:
            try:
                logging.exception(ex)
            finally:
                ex = None
                del ex

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            form_data = json.loads(slc.params)
            if 'time_range' in form_data:
                try:
                    since, until = form_data['time_range'].split(' : ')
                    form_data['since'] = since
                    form_data['until'] = until
                    del form_data['time_range']
                    slc.params = json.dumps(form_data, sort_keys=True)
                except ValueError:
                    pass

        except Exception as ex:
            try:
                logging.exception(ex)
            finally:
                ex = None
                del ex

    session.commit()