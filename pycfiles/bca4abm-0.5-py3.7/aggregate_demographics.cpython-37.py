# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\four_step\aggregate_demographics.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 2825 bytes
import logging, os, pandas as pd, numpy as np
from bca4abm import bca4abm as bca
from util.misc import add_aggregate_results
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import assign
from activitysim.core import pipeline
logger = logging.getLogger(__name__)

@inject.injectable()
def aggregate_demographics_spec():
    return bca.read_assignment_spec('aggregate_demographics.csv')


@inject.step()
def aggregate_demographics_processor(zone_hhs, aggregate_demographics_spec, settings, trace_od):
    """

    Parameters
    ----------
    zone_hhs : orca table
        input zone demographics

    """
    trace_label = 'aggregate_demographics'
    model_settings = config.read_model_settings('aggregate_demographics.yaml')
    zone_hhs_df = zone_hhs.to_frame()
    logger.info('Running %s with %d zones' % (trace_label, len(zone_hhs_df)))
    if trace_od:
        trace_orig, trace_dest = trace_od
        trace_od_rows = (zone_hhs_df.index == trace_orig) | (zone_hhs_df.index == trace_dest)
    else:
        trace_od_rows = None
    locals_dict = config.get_model_constants(model_settings)
    locals_dict.update(config.setting('globals'))
    trace_rows = None
    results, trace_results, trace_assigned_locals = assign.assign_variables(aggregate_demographics_spec, zone_hhs_df,
      locals_dict,
      df_alias='hhs',
      trace_rows=trace_od_rows)
    pipeline.replace_table('zone_demographics', results)
    add_aggregate_results(results, aggregate_demographics_spec, source=trace_label)
    if trace_results is not None:
        tracing.write_csv(trace_results, file_name='aggregate_demographics',
          index_label='zone',
          column_labels=[
         'label', 'zone'])
        if trace_assigned_locals:
            tracing.write_csv(trace_assigned_locals, file_name='aggregate_demographics_locals')