# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\four_step\aggregate_zone.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 3297 bytes
import logging, os, pandas as pd, numpy as np
from bca4abm import bca4abm as bca
from util.misc import add_aggregate_results
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import assign
from activitysim.core import pipeline
logger = logging.getLogger(__name__)

@inject.step()
def aggregate_zone_processor(zones, trace_od):
    """
    zones: orca table

    zone data for base and build scenario dat files combined into a single dataframe
    with columns names prefixed with base_ or build_ indexed by ZONE
    """
    trace_label = 'aggregate_zone'
    model_settings = config.read_model_settings('aggregate_zone.yaml')
    spec_file_name = model_settings.get('spec_file_name', 'aggregate_zone.csv')
    aggregate_zone_spec = bca.read_assignment_spec(spec_file_name)
    zones_df = zones.to_frame()
    logger.info('Running aggregate_zone_processor with %d zones' % (
     len(zones_df.index),))
    if trace_od:
        trace_orig, trace_dest = trace_od
        trace_od_rows = (zones_df.index == trace_orig) | (zones_df.index == trace_dest)
    else:
        trace_od_rows = None
    locals_dict = config.get_model_constants(model_settings)
    locals_dict.update(config.setting('globals'))
    results, trace_results, trace_assigned_locals = assign.assign_variables(aggregate_zone_spec, zones_df,
      locals_dict,
      df_alias='zones',
      trace_rows=trace_od_rows)
    pipeline.replace_table('aggregate_zone_summary', results)
    if trace_results is not None:
        tracing.write_csv(trace_results, file_name='aggregate_zone',
          index_label='zone',
          column_labels=[
         'label', 'zone'])
        if trace_assigned_locals:
            tracing.write_csv(trace_assigned_locals, file_name='aggregate_zone_locals')


@inject.step()
def aggregate_zone_benefits(aggregate_zone_summary):
    trace_label = 'aggregate_zone_benefits'
    zone_summary = aggregate_zone_summary.to_frame()
    model_settings = config.read_model_settings('aggregate_zone.yaml')
    spec_file_name = model_settings.get('spec_file_name', 'aggregate_zone.csv')
    aggregate_zone_spec = bca.read_assignment_spec(spec_file_name)
    add_aggregate_results(zone_summary, aggregate_zone_spec, source=trace_label)