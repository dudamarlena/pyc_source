# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\abm\person_trips.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 2673 bytes
import logging, os, pandas as pd
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import assign
from bca4abm import bca4abm as bca
from util.misc import add_result_columns, add_summary_results
logger = logging.getLogger(__name__)

@inject.injectable()
def person_trips_spec():
    return bca.read_assignment_spec('person_trips.csv')


@inject.injectable()
def person_trips_settings():
    return config.read_model_settings('person_trips.yaml')


@inject.step()
def person_trips_processor(trips_with_demographics, person_trips_spec, person_trips_settings, coc_column_names, settings, chunk_size, trace_hh_id):
    """
    Compute disaggregate trips benefits
    """
    trips_df = trips_with_demographics.to_frame()
    logger.info('Running person_trips_processor with %d trips (chunk size = %s)' % (
     len(trips_with_demographics), chunk_size))
    locals_dict = config.get_model_constants(person_trips_settings)
    locals_dict.update(config.setting('globals'))
    locals_dict['trips'] = trips_df
    trace_rows = trace_hh_id and trips_df['household_id'] == trace_hh_id
    coc_summary, trace_results, trace_assigned_locals = bca.eval_and_sum(assignment_expressions=person_trips_spec, df=trips_df,
      locals_dict=locals_dict,
      df_alias='trips',
      group_by_column_names=coc_column_names,
      chunk_size=chunk_size,
      trace_rows=trace_rows)
    result_prefix = 'PT_'
    add_result_columns('coc_results', coc_summary, result_prefix)
    add_summary_results(coc_summary, prefix=result_prefix, spec=person_trips_spec)
    if trace_hh_id:
        if trace_results is not None:
            tracing.write_csv(trace_results, file_name='person_trips',
              index_label='trip_id',
              column_labels=[
             'label', 'trip'])
        if trace_assigned_locals:
            tracing.write_csv(trace_assigned_locals, file_name='person_trips_locals')