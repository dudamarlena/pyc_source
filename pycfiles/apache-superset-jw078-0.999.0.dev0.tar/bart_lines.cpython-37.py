# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/bart_lines.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2148 bytes
import json, pandas as pd, polyline
from sqlalchemy import String, Text
from superset import db
from superset.utils.core import get_example_database
from .helpers import get_example_data, TBL

def load_bart_lines(only_metadata=False, force=False):
    tbl_name = 'bart_lines'
    database = get_example_database()
    table_exists = database.has_table_by_name(tbl_name)
    if not only_metadata:
        if not table_exists or force:
            content = get_example_data('bart-lines.json.gz')
            df = pd.read_json(content, encoding='latin-1')
            df['path_json'] = df.path.map(json.dumps)
            df['polyline'] = df.path.map(polyline.encode)
            del df['path']
            df.to_sql(tbl_name,
              (database.get_sqla_engine()),
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
    tbl.database = database
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()