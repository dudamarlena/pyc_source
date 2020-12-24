# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/ab8c66efdd01_resample.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 3648 bytes
__doc__ = 'resample\n\nRevision ID: ab8c66efdd01\nRevises: d7c1a0d6f2da\nCreate Date: 2019-06-28 13:17:59.517089\n\n'
revision = 'ab8c66efdd01'
down_revision = 'd7c1a0d6f2da'
import json, logging
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
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
            params = json.loads(slc.params)
            if 'resample_rule' in params:
                rule = params['resample_rule']
                if rule:
                    how = None
                    if 'resample_how' in params:
                        how = params['resample_how']
                        if how:
                            params['resample_method'] = how
                    if not how:
                        if 'fill_method' in params:
                            fill_method = params['resample_fillmethod']
                            if fill_method:
                                params['resample_method'] = fill_method
                    if 'resample_method' not in params:
                        del params['resample_rule']
                else:
                    del params['resample_rule']
                params.pop('resample_fillmethod', None)
                params.pop('resample_how', None)
                slc.params = json.dumps(params, sort_keys=True)
        except Exception as e:
            try:
                logging.exception(e)
            finally:
                e = None
                del e

    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            params = json.loads(slc.params)
            if 'resample_method' in params:
                method = params['resample_method']
                if method in ('asfreq', 'bfill', 'ffill'):
                    params['resample_fillmethod'] = method
                else:
                    params['resample_how'] = method
                del params['resample_method']
                slc.params = json.dumps(params, sort_keys=True)
        except Exception as e:
            try:
                logging.exception(e)
            finally:
                e = None
                del e

    session.commit()
    session.close()