# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\four_step\aggregate_od.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 11122 bytes
from builtins import object
import logging, os, psutil, re, pandas as pd, numpy as np, openmatrix as omx
from bca4abm import bca4abm as bca
from util.misc import add_aggregate_results
from activitysim.core import config
from activitysim.core import inject
from activitysim.core import tracing
from activitysim.core import pipeline
from activitysim.core import assign
logger = logging.getLogger(__name__)

def memory_info():

    def GB(bytes):
        gb = bytes / 1073741824.0
        return '%s GB' % (round(gb, 2),)

    mi = psutil.Process().memory_full_info()
    return 'memory_info: vms: %s rss: %s uss: %s' % (GB(mi.vms), GB(mi.rss), GB(mi.uss))


class ODSkims(object):
    __doc__ = '\n    Wrapper for skim arrays to facilitate use of skims by aggregate_od_processor\n\n    Parameters\n    ----------\n    skims_dict : empty dict to cache skims read from file\n    omx: open omx file object\n        this is only used to load skims on demand that were not preloaded\n    length: int\n        number of zones in skim to return in skim matrix\n        in case the skims contain additional external zones that should be trimmed out so skim\n        array is correct shape to match (flattened) O-D tiled columns in the od dataframe\n    transpose: bool\n        whether to transpose the matrix before flattening. (i.e. act as a D-O instead of O-D skim)\n    '

    def __init__(self, omx_file_path, name, zone_index, transpose=False, cache_skims=True):
        self.skims = {}
        self.name = name
        self.transpose = transpose
        self.omx = omx.open_file(omx_file_path, 'r')
        self.omx_shape = tuple([int(s) for s in self.omx.shape()])
        self.length = zone_index.shape[0]
        assert self.omx_shape[0] == self.length
        assert self.omx_shape[1] == self.length
        self.skim_dtype = np.float64
        self.cache_skims = cache_skims
        self.usage = {key:0 for key in self.omx.listMatrices()}
        logger.debug('omx file %s skim shape: %s number of skims: %s' % (
         name, self.omx_shape, len(self.usage)))

    def __getitem__(self, key):
        """
        accessor to return flattened skim array with specified key
        flattened array will have length length*length and will match tiled OD df used by asim_eval

        this allows the skim array to be accessed from expressions as
        skim['DISTANCE'] or skim[('SOVTOLL_TIME', 'MD')]
        """
        if not key in self.usage:
            raise AssertionError
        else:
            self.usage[key] += 1
            if key in self.skims:
                data = self.skims[key]
            else:
                data = self.get_from_omx(key)
                if self.cache_skims:
                    self.skims[key] = data
        return data

    def get_from_omx(self, key):
        if isinstance(key, str):
            omx_key = key
        else:
            if isinstance(key, tuple):
                omx_key = '__'.join(key)
            else:
                raise RuntimeError('Unexpected skim key type %s' % type(key))
        try:
            data = self.omx[omx_key][:self.length, :self.length]
        except omx.tables.exceptions.NoSuchNodeError:
            raise RuntimeError("Could not find skim with key '%s' in %s" % (omx_key, self.name))

        if self.transpose:
            data = data.transpose()
        return data.flatten()

    def log_skim_usage(self):
        num_skims = len(self.usage)
        num_used = (np.asanyarray(list(self.usage.values())) > 0).sum()
        num_unused = num_skims - num_used
        avg_used = np.asanyarray(list(self.usage.values())).sum() / float(num_used or 1)
        max_used = np.asanyarray(list(self.usage.values())).max()
        logger.debug('  %s (cached=%s) %s skims in omx file %s used (%s avg %s max) %s unused' % (
         self.name, self.cache_skims,
         num_skims, num_used, avg_used, max_used, num_unused))
        for key, n in self.usage.items():
            logger.info('%s.%s %s' % (self.name, key, n))

    def close(self):
        self.omx.close()
        self.skims = {}


def create_skim_locals_dict(model_settings, data_dir, zones_df, cache_skims):
    zone_index = zones_df.index
    aggregate_od_matrices = model_settings.get('aggregate_od_matrices', None)
    if not aggregate_od_matrices:
        raise RuntimeError('No list of aggregate_od_matrices found in model_settings')
    local_od_skims = {}
    for local_name, omx_file_name in aggregate_od_matrices.items():
        for scenario in ('base', 'build'):
            full_local_name = '_'.join([local_name, scenario])
            data_sub_dir = '%s-data' % scenario
            omx_file_path = os.path.join(data_dir, data_sub_dir, omx_file_name)
            logger.debug('add od_skims to locals: %s : %s' % (full_local_name, omx_file_name))
            skims = ODSkims(omx_file_path=omx_file_path, name=full_local_name,
              zone_index=zone_index,
              cache_skims=cache_skims)
            local_od_skims[full_local_name] = skims

    return local_od_skims


def create_zone_matrices(model_settings, zones):
    """
    ODSkims look-alikes that have identical values for all zone origins/dests

    i.e. we either repeat (origin_zone_matrices) or tile (dest_zone_matrices) zone values
    to expand zones columns into ODSkims-style flattened arrays
    """

    def zone_matrices(column_list_key, rep_func):
        dict = {}
        columns = model_settings.get(column_list_key, [])
        for scenario in ('base', 'build'):
            for c in columns:
                zones_col = '%s_%s' % (scenario, c)
                dict_col = '%s_%s' % (c, scenario)
                if zones_col not in zones:
                    raise RuntimeError("%s column '%s' not found in zones table" % (
                     column_list_key, zones_col))
                dict[dict_col] = rep_func(zones[('%s_%s' % (scenario, c))].values, zones.shape[0])

        return dict

    zone_matrix_dict = {}
    zone_matrix_dict['origin_zone'] = zone_matrices('origin_zone_matrices', np.repeat)
    zone_matrix_dict['dest_zone'] = zone_matrices('dest_zone_matrices', np.tile)
    return zone_matrix_dict


@inject.step()
def aggregate_od_processor(zone_districts, zones, data_dir, trace_od):
    trace_label = 'aggregate_od'
    logger.info('Running %s' % (trace_label,))
    model_settings = config.read_model_settings('aggregate_od.yaml')
    spec_file_name = model_settings.get('spec_file_name', 'aggregate_od.csv')
    aggregate_od_spec = bca.read_assignment_spec(spec_file_name)
    zones = zones.to_frame()
    zone_districts = zone_districts.to_frame()
    zone_count = zone_districts.shape[0]
    if not zones.index.equals(zone_districts.index):
        raise AssertionError
    else:
        od_df = pd.DataFrame(data={'orig':np.repeat(np.asanyarray(zones.index), zone_count), 
         'dest':np.tile(np.asanyarray(zones.index), zone_count)})
        locals_dict = config.get_model_constants(model_settings)
        locals_dict.update(config.setting('globals'))
        locals_dict['logger'] = logger
        logger.debug('%s mem before create_skim_locals_dict, %s' % (trace_label, memory_info()))
        cache_skims = model_settings.get('cache_skims', False)
        local_skims = create_skim_locals_dict(model_settings, data_dir, zones, cache_skims)
        locals_dict.update(local_skims)
        locals_dict.update(create_zone_matrices(model_settings, zones))
        if trace_od:
            trace_orig, trace_dest = trace_od
            trace_od_rows = (od_df.orig == trace_orig) & (od_df.dest == trace_dest)
        else:
            trace_od_rows = None
    logger.debug('%s assigning variables' % (trace_label,))
    results, trace_results, trace_assigned_locals = assign.assign_variables(aggregate_od_spec, od_df,
      locals_dict=locals_dict,
      df_alias='od',
      trace_rows=trace_od_rows)
    logger.debug('%s mem after assign_variables, %s' % (trace_label, memory_info()))
    for local_name, od_skims in local_skims.items():
        logger.debug('closing %s' % local_name)
        od_skims.log_skim_usage()
        od_skims.close()

    logger.debug('%s district summary' % (trace_label,))
    results['orig'] = np.repeat(np.asanyarray(zone_districts.district), zone_count)
    results['dest'] = np.tile(np.asanyarray(zone_districts.district), zone_count)
    district_summary = results.groupby(['orig', 'dest']).sum()
    pipeline.replace_table('aggregate_od_district_summary', district_summary)
    logger.debug('%s zone summary' % (trace_label,))
    results['orig'] = od_df['orig']
    del results['dest']
    zone_summary = results.groupby(['orig']).sum()
    pipeline.replace_table('aggregate_od_zone_summary', zone_summary)
    add_aggregate_results(zone_summary, aggregate_od_spec, source=trace_label)
    if trace_results is not None:
        tracing.write_csv(trace_results, file_name=trace_label,
          index_label='index',
          column_labels=[
         'label', 'od'])
        if trace_assigned_locals:
            tracing.write_csv(trace_assigned_locals, file_name=('%s_locals' % trace_label),
              index_label='variable',
              columns='value')