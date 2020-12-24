# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\tables\trips.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 3310 bytes
import logging, pandas as pd
from activitysim.core import inject
from activitysim.core import config
from bca4abm import bca4abm as bca
logger = logging.getLogger(__name__)

def read_merged_trips(table_name, alt_table_name, data_dir, table_settings, persons):
    trips = bca.read_csv_table(table_name=table_name, data_dir=data_dir, settings=table_settings)
    trips_alt = bca.read_csv_table(table_name=alt_table_name, data_dir=data_dir, settings=table_settings)
    trips_merged = pd.merge(trips, trips_alt, on=['household_id',
     'person_idx',
     'tour_idx',
     'half_tour_idx',
     'half_tour_seg_idx'])
    persons = persons.to_frame()[['household_id', 'person_idx']]
    persons['person_id'] = persons.index
    trips_merged = pd.merge(trips_merged, persons, on=['household_id', 'person_idx'])
    return trips_merged


@inject.table()
def base_trips(data_dir, persons):
    logger.debug('reading base_trips table')
    table_settings = config.read_model_settings('tables.yaml')
    trips_merged = read_merged_trips(table_name='basetrips', alt_table_name='basetrips_buildlos',
      data_dir=data_dir,
      table_settings=table_settings,
      persons=persons)
    trips_merged['build'] = 0
    trips_merged['base'] = 1
    return trips_merged


@inject.table()
def build_trips(data_dir, persons):
    logger.debug('reading build_trips table')
    table_settings = config.read_model_settings('tables.yaml')
    trips_merged = read_merged_trips(table_name='buildtrips', alt_table_name='buildtrips_baselos',
      data_dir=data_dir,
      table_settings=table_settings,
      persons=persons)
    trips_merged['build'] = 1
    trips_merged['base'] = 0
    return trips_merged


@inject.table()
def disaggregate_trips(base_trips, build_trips):
    build = build_trips.to_frame()
    base = base_trips.to_frame()
    df = base.append(build, ignore_index=True, sort=False)
    df['index1'] = df.index
    return df


inject.broadcast(cast='persons_merged', onto='disaggregate_trips',
  cast_index=True,
  onto_on='person_id')

@inject.table()
def trips_with_demographics(disaggregate_trips, persons_merged):
    return inject.merge_tables(target=(disaggregate_trips.name), tables=[
     disaggregate_trips, persons_merged])