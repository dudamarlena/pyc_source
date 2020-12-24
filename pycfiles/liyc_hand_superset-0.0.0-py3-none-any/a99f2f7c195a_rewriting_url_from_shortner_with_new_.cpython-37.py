# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\a99f2f7c195a_rewriting_url_from_shortner_with_new_.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 2490 bytes
"""rewriting url from shortner with new format

Revision ID: a99f2f7c195a
Revises: 53fc3de270ae
Create Date: 2017-02-08 14:16:34.948793

"""
revision = 'a99f2f7c195a'
down_revision = 'db0c65b146bd'
from alembic import op
import json, sqlalchemy as sa
from superset import db
from sqlalchemy.ext.declarative import declarative_base
from urllib import parse
Base = declarative_base()

def parse_querystring(qs):
    d = {}
    for k, v in parse.parse_qsl(qs):
        if k not in d:
            d[k] = v
        elif isinstance(d[k], list):
            d[k].append(v)
        else:
            d[k] = [
             d[k], v]

    return d


class Url(Base):
    __doc__ = 'Used for the short url feature'
    __tablename__ = 'url'
    id = sa.Column((sa.Integer), primary_key=True)
    url = sa.Column(sa.Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    urls = session.query(Url).all()
    urls_len = len(urls)
    for i, url in enumerate(urls):
        if '?form_data' not in url.url:
            if '?' in url.url:
                if 'dbid' not in url.url:
                    if url.url.startswith('//superset/explore'):
                        d = parse_querystring(url.url.split('?')[1])
                        split = url.url.split('/')
                        d['datasource'] = split[5] + '__' + split[4]
                        newurl = '/'.join(split[:-1]) + '/?form_data=' + parse.quote_plus(json.dumps(d))
                        url.url = newurl
                        session.merge(url)
                        session.commit()
        print('Updating url ({}/{})'.format(i, urls_len))

    session.close()


def downgrade():
    pass