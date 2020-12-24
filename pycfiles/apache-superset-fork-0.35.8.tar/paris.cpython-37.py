# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/paris.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2039 bytes
import json, pandas as pd
from sqlalchemy import String, Text
from superset import db
import superset.utils as utils
from .helpers import get_example_data, TBL

def load_paris_iris_geojson(only_metadata=False, force=False):
    tbl_name = 'paris_iris_mapping'
    database = utils.get_example_database()
    table_exists = database.has_table_by_name(tbl_name)
    if not only_metadata:
        if not table_exists or force:
            data = get_example_data('paris_iris.json.gz')
            df = pd.read_json(data)
            df['features'] = df.features.map(json.dumps)
            df.to_sql(tbl_name,
              (database.get_sqla_engine()),
              if_exists='replace',
              chunksize=500,
              dtype={'color':String(255), 
             'name':String(255), 
             'features':Text, 
             'type':Text},
              index=False)
    print('Creating table {} reference'.format(tbl_name))
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = 'Map of Paris'
    tbl.database = database
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()