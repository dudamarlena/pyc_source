# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\abm\demographics.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 3521 bytes
import logging, os, pandas as pd
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import assign
from activitysim.core import pipeline
from bca4abm import bca4abm as bca
from util.misc import add_result_columns, add_summary_results
from activitysim.core.util import assign_in_place
logger = logging.getLogger(__name__)

@inject.injectable()
def demographics_spec():
    return bca.read_assignment_spec('demographics.csv')


@inject.injectable()
def demographics_settings():
    return config.read_model_settings('demographics.yaml')


@inject.step()
def demographics_processor(persons, persons_merged, demographics_spec, demographics_settings, chunk_size, trace_hh_id):
    persons_df = persons_merged.to_frame()
    logger.info('Running demographics_processor with %d persons (chunk size = %s)' % (
     len(persons_df), chunk_size))
    locals_dict = config.get_model_constants(demographics_settings)
    locals_dict.update(config.setting('globals'))
    trace_rows = trace_hh_id and persons_df['household_id'] == trace_hh_id
    results, trace_results, trace_assigned_locals = assign.assign_variables(demographics_spec, persons_df,
      locals_dict,
      df_alias='persons',
      trace_rows=trace_rows)
    persons = persons.to_frame()
    assign_in_place(persons, results)
    pipeline.replace_table('persons', persons)
    coc_columns = list(results.columns)
    inject.add_injectable('coc_column_names', coc_columns)
    coc_grouped = results.groupby(coc_columns)
    coc_grouped = coc_grouped[coc_columns[0]].count().to_frame(name='persons')
    pipeline.replace_table('coc_results', coc_grouped)
    add_summary_results(coc_grouped)
    if trace_hh_id:
        if trace_results is not None:
            tracing.write_csv(trace_results, file_name='demographics',
              index_label='person_idx',
              column_labels=[
             'label', 'person'])
        if trace_assigned_locals:
            tracing.write_csv(trace_assigned_locals, file_name='demographics_locals')