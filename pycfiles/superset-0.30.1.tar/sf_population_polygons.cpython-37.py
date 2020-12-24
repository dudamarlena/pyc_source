# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/data/sf_population_polygons.py
# Compiled at: 2019-05-15 12:58:52
# Size of source mod 2**32: 1828 bytes
import json, pandas as pd
from sqlalchemy import BigInteger, Text
from superset import db
import superset.utils as utils
from .helpers import TBL, get_example_data

def load_sf_population_polygons():
    tbl_name = 'sf_population_polygons'
    data = get_example_data('sf_population.json.gz')
    df = pd.read_json(data)
    df['contour'] = df.contour.map(json.dumps)
    df.to_sql(tbl_name,
      (db.engine),
      if_exists='replace',
      chunksize=500,
      dtype={'zipcode':BigInteger, 
     'population':BigInteger, 
     'contour':Text, 
     'area':BigInteger},
      index=False)
    print('Creating table {} reference'.format(tbl_name))
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = 'Population density of San Francisco'
    tbl.database = utils.get_or_create_main_db()
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()