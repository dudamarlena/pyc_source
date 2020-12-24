# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/data/bart_lines.py
# Compiled at: 2019-05-15 12:58:52
# Size of source mod 2**32: 1882 bytes
import json, pandas as pd, polyline
from sqlalchemy import String, Text
from superset import db
from superset.utils.core import get_or_create_main_db
from .helpers import TBL, get_example_data

def load_bart_lines():
    tbl_name = 'bart_lines'
    content = get_example_data('bart-lines.json.gz')
    df = pd.read_json(content, encoding='latin-1')
    df['path_json'] = df.path.map(json.dumps)
    df['polyline'] = df.path.map(polyline.encode)
    del df['path']
    df.to_sql(tbl_name,
      (db.engine),
      if_exists='replace',
      chunksize=500,
      dtype={'color':String(255), 
     'name':String(255), 
     'polyline':Text, 
     'path_json':Text},
      index=False)
    print('Creating table {} reference'.format(tbl_name))
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = 'BART lines'
    tbl.database = get_or_create_main_db()
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()