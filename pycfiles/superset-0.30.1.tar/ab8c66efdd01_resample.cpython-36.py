# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/ab8c66efdd01_resample.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 3648 bytes
"""resample

Revision ID: ab8c66efdd01
Revises: d7c1a0d6f2da
Create Date: 2019-06-28 13:17:59.517089

"""
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
            logging.exception(e)

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
            logging.exception(e)

    session.commit()
    session.close()