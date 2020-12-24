# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\abm\auto_ownership.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 2353 bytes
import logging, os, pandas as pd
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import assign
from bca4abm import bca4abm as bca
from util.misc import add_result_columns, add_summary_results
logger = logging.getLogger(__name__)

@inject.injectable()
def auto_ownership_spec():
    return bca.read_assignment_spec('auto_ownership.csv')


@inject.injectable()
def auto_ownership_settings():
    return config.read_model_settings('auto_ownership.yaml')


@inject.step()
def auto_ownership_processor(persons_merged, auto_ownership_spec, auto_ownership_settings, coc_column_names, chunk_size, trace_hh_id):
    """
    Compute auto ownership benefits
    """
    persons_df = persons_merged.to_frame()
    logger.info('Running auto_ownership_processor with %d persons (chunk size = %s)' % (
     len(persons_df), chunk_size))
    locals_dict = config.get_model_constants(auto_ownership_settings)
    locals_dict.update(config.setting('globals'))
    trace_rows = trace_hh_id and persons_df['household_id'] == trace_hh_id
    coc_summary, trace_results, trace_assigned_locals = bca.eval_and_sum(assignment_expressions=auto_ownership_spec, df=persons_df,
      locals_dict=locals_dict,
      df_alias='persons',
      group_by_column_names=coc_column_names,
      chunk_size=chunk_size,
      trace_rows=trace_rows)
    result_prefix = 'AO_'
    add_result_columns('coc_results', coc_summary, result_prefix)
    add_summary_results(coc_summary, prefix=result_prefix, spec=auto_ownership_spec)
    if trace_hh_id:
        if trace_results is not None:
            tracing.write_csv(trace_results, file_name='auto_ownership',
              index_label='person_id',
              column_labels=[
             'label', 'person'])
        if trace_assigned_locals:
            tracing.write_csv(trace_assigned_locals, file_name='auto_ownership_locals')