# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\abm\physical_activity.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 7886 bytes
import logging, pandas as pd
from bca4abm import bca4abm as bca
from util.misc import add_result_columns, add_summary_results
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import assign
from activitysim.core import chunk
logger = logging.getLogger(__name__)

@inject.injectable()
def physical_activity_trip_spec():
    return bca.read_assignment_spec('physical_activity_trip.csv')


@inject.injectable()
def physical_activity_person_spec():
    return bca.read_assignment_spec('physical_activity_person.csv')


@inject.injectable()
def physical_activity_settings():
    return config.read_model_settings('physical_activity.yaml')


def physical_activity_rpc(chunk_size, trips_df, persons_df, spec, trace_label=None):
    num_chunk_ids = trips_df['chunk_id'].max() + 1
    if chunk_size == 0:
        return num_chunk_ids
    spec_temps = spec.target.str.match('_').sum()
    spec_vars = spec.shape[0] - spec_temps
    trip_row_size = trips_df.shape[1] + spec_vars
    trip_rows_per_chunk_id = trips_df.shape[0] / float(num_chunk_ids)
    persons_row_size = persons_df.shape[1]
    persons_rows_per_chunk_id = persons_df.shape[0] / float(num_chunk_ids)
    row_size = trip_rows_per_chunk_id * trip_row_size + persons_rows_per_chunk_id * persons_row_size
    return chunk.rows_per_chunk(chunk_size, row_size, num_chunk_ids, trace_label)


@inject.step()
def physical_activity_processor(trips_with_demographics, persons_merged, physical_activity_trip_spec, physical_activity_person_spec, physical_activity_settings, coc_column_names, settings, chunk_size, trace_hh_id):
    """
    Compute physical benefits

    Physical activity benefits generally accrue if the net physical activity for an individual
    exceeds a certain threshold. We calculate individual physical activity based on trips,
    so we need to compute trip activity and then sum up to the person level to calculate benefits.
    We chunk trips by household id to ensure that all of a persons trips are in the same chunk.
    """
    trips_df = trips_with_demographics.to_frame()
    persons_df = persons_merged.to_frame()
    trace_label = 'physical_activity'
    logger.info('Running physical_activity_processor with %d trips for %d persons ' % (
     len(trips_df), len(persons_df)))
    locals_dict = config.get_model_constants(physical_activity_settings)
    locals_dict.update(config.setting('globals'))
    trip_trace_rows = trace_hh_id and trips_df.household_id == trace_hh_id
    rows_per_chunk, effective_chunk_size = physical_activity_rpc(chunk_size, trips_df, persons_df, physical_activity_trip_spec, trace_label)
    logger.info('physical_activity_processor chunk_size %s rows_per_chunk %s' % (
     chunk_size, rows_per_chunk))
    coc_summary = None
    result_list = []
    for i, num_chunks, trips_chunk, trace_rows_chunk in bca.chunked_df_by_chunk_id(trips_df, trip_trace_rows, rows_per_chunk):
        logger.info('%s chunk %s of %s' % (trace_label, i, num_chunks))
        trip_activity, trip_trace_results, trip_trace_assigned_locals = assign.assign_variables(physical_activity_trip_spec, trips_chunk,
          locals_dict=locals_dict,
          df_alias='trips',
          trace_rows=trace_rows_chunk)
        if trip_trace_results is not None:
            tracing.write_csv(trip_trace_results, file_name='physical_activity_trips',
              index_label='trip_id',
              column_labels=[
             'label', 'trip'])
            if trip_trace_assigned_locals:
                tracing.write_csv(trip_trace_assigned_locals, file_name='physical_activity_trips_locals')
        trip_activity = trip_activity.groupby(trips_chunk.person_id).sum()
        persons_chunk = pd.merge(trip_activity, persons_df, left_index=True,
          right_index=True)
        person_trace_rows = trace_hh_id and persons_chunk['household_id'] == trace_hh_id
        person_activity, person_trace_results, person_trace_assigned_locals = assign.assign_variables(physical_activity_person_spec, persons_chunk,
          locals_dict=locals_dict,
          df_alias='persons',
          trace_rows=person_trace_rows)
        if person_trace_results is not None:
            tracing.write_csv(person_trace_results, file_name='physical_activity_persons',
              index_label='persons_merged_table_index',
              column_labels=[
             'label', 'person'])
            if person_trace_assigned_locals:
                tracing.write_csv(person_trace_assigned_locals, file_name='physical_activity_persons_locals')
        person_activity = pd.concat([persons_chunk[coc_column_names], person_activity], axis=1)
        coc_summary = person_activity.groupby(coc_column_names).sum()
        result_list.append(coc_summary)
        chunk_trace_label = 'trace_label chunk_%s' % i
        chunk.log_open(chunk_trace_label, chunk_size, effective_chunk_size)
        chunk.log_df(chunk_trace_label, 'trips_chunk', trips_chunk)
        chunk.log_df(chunk_trace_label, 'persons_chunk', persons_chunk)
        chunk.log_close(chunk_trace_label)

    if len(result_list) > 1:
        coc_summary = pd.concat(result_list)
        coc_summary.reset_index(inplace=True)
        coc_summary = coc_summary.groupby(coc_column_names).sum()
    result_prefix = 'PA_'
    add_result_columns('coc_results', coc_summary, result_prefix)
    add_summary_results(coc_summary, prefix=result_prefix, spec=physical_activity_person_spec)