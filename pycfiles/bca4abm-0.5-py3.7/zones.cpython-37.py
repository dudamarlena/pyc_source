# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\tables\zones.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 7663 bytes
from builtins import range
import logging, os.path, numpy as np, pandas as pd, itertools
from activitysim.core import inject
from activitysim.core import config
from activitysim.core import tracing
from bca4abm import bca4abm as bca
logger = logging.getLogger(__name__)

def read_csv_file(data_dir, file_name):
    fpath = os.path.join(data_dir, file_name)
    df = bca.read_csv_or_tsv(fpath, header=0, comment='#')
    return df


def read_zone_indexed_csv_file(data_dir, file_name, zone_aliases, zone_ids_index):
    fpath = os.path.join(data_dir, file_name)
    logger.info('read zone indexed csv file: ' + fpath)
    df = bca.read_csv_or_tsv(fpath, header=0, comment='#').rename(columns=zone_aliases)
    if zone_ids_index is not None:
        if 'zone' in df:
            assert (zone_ids_index == df.zone.values).all()
            df.set_index('zone', drop=True, inplace=True)
        else:
            df.index = zone_ids_index
    else:
        df.index = df.index + 1
        if 'zone' in df:
            assert (df.index.values == list(range(1, len(df) + 1))).all()
    df.index.name = 'ZONE'
    return df


def read_and_concat_zone_indexed_csv_files(data_dir, file_names, zone_aliases, zone_ids_index):
    """

    Parameters
    ----------
    data_dir
    file_names
    zone_aliases
    zone_ids_index

    Returns
    -------
        omnibus_df: pandas df
            df with all the columns from file list (except zone ids)
            with index named 'zone' if zone_ids_index supplied
            otherwise, zero-based default index
    """
    omnibus_df = None
    for file_name in file_names:
        df = read_zone_indexed_csv_file(data_dir, file_name, zone_aliases, zone_ids_index)
        if omnibus_df is None:
            omnibus_df = df
        else:
            omnibus_df = pd.concat([omnibus_df, df], axis=1)

    return omnibus_df


def check_zone_index(df, zone_ids):
    if zone_ids is not None:
        expected_index = zone_ids.values
    else:
        expected_index = list(range(1, len(df) + 1))
    assert (df.index.values == expected_index).all()
    assert df.index.name == 'ZONE'


@inject.table()
def zone_districts(data_dir, zone_aliases, zone_ids):
    table_settings = config.read_model_settings('tables.yaml')
    file_name = table_settings.get('district_file_name')
    districts_df = read_zone_indexed_csv_file(data_dir, file_name, zone_aliases, zone_ids)
    assert 'district' in districts_df
    check_zone_index(districts_df, zone_ids)
    tracing.write_csv(districts_df, file_name='zone_districts',
      transpose=False)
    return districts_df


@inject.table()
def zone_hhs(data_dir, zone_aliases, zone_ids):
    logger.debug('reading zone_hhs table')
    table_settings = config.read_model_settings('tables.yaml')
    file_name = table_settings.get('hh_file_name')
    base_data_dir = os.path.join(data_dir, 'base-data')
    build_data_dir = os.path.join(data_dir, 'build-data')
    base_hhs_df = read_zone_indexed_csv_file(base_data_dir, file_name, zone_aliases, zone_ids)
    build_hhs_df = read_zone_indexed_csv_file(build_data_dir, file_name, zone_aliases, zone_ids)
    cocs_file_name = table_settings.get('ext_cocs_file_name')
    base_cocs_df = read_zone_indexed_csv_file(base_data_dir, cocs_file_name, zone_aliases, zone_ids)
    base_hhs_df = pd.concat([base_hhs_df, base_cocs_df], axis=1)
    build_cocs_df = read_zone_indexed_csv_file(build_data_dir, cocs_file_name, zone_aliases, zone_ids)
    build_hhs_df = pd.concat([build_hhs_df, build_cocs_df], axis=1)
    base_hhs_df.columns = ['base_%s' % c for c in base_hhs_df.columns.values]
    build_hhs_df.columns = ['build_%s' % c for c in build_hhs_df.columns.values]
    hhs_df = pd.concat([base_hhs_df, build_hhs_df], axis=1)
    check_zone_index(hhs_df, zone_ids)
    tracing.write_csv(hhs_df, file_name='zone_hhs',
      transpose=False)
    return hhs_df


@inject.table()
def zones(data_dir, zone_aliases, zone_ids):
    """
    aggregate_zone_file_names in settings contains a list of file name
    for zones table csv data input files (expect versions in build and base data subdirs)
    data will be combined into a single table with columns names prefixed with 'base_' or 'build_'
    (e.g.) if ma.hbcdcls.csv has a column 'hbcdcls' you will have 'base_hbcdcls' and 'build_hbcdcls'
    """
    logger.debug('reading zones table')
    table_settings = config.read_model_settings('tables.yaml')
    file_names = table_settings.get('aggregate_zone_file_names')
    base_zones_df = read_and_concat_zone_indexed_csv_files(data_dir=(os.path.join(data_dir, 'base-data')),
      file_names=file_names,
      zone_aliases=zone_aliases,
      zone_ids_index=zone_ids)
    build_zones_df = read_and_concat_zone_indexed_csv_files(data_dir=(os.path.join(data_dir, 'build-data')),
      file_names=file_names,
      zone_aliases=zone_aliases,
      zone_ids_index=zone_ids)
    assert base_zones_df.index.equals(build_zones_df.index)
    base_zones_df.columns = ['base_%s' % c for c in base_zones_df.columns.values]
    build_zones_df.columns = ['build_%s' % c for c in build_zones_df.columns.values]
    zones_df = pd.concat([base_zones_df, build_zones_df], axis=1)
    check_zone_index(zones_df, zone_ids)
    tracing.write_csv(zones_df, file_name='zones',
      transpose=False)
    return zones_df


@inject.injectable(cache=True)
def zone_aliases():
    table_settings = config.read_model_settings('tables.yaml')
    aliases = table_settings.get('zone_aliases', [])
    aliases = {a:'zone' for a in aliases}
    return aliases


@inject.injectable(cache=True)
def zone_ids(data_dir, zone_aliases):
    """
    we require a master zone_ids file for anything but default 1-based contiguous zone ids
    it could be specified in the zone_districts file, but we we want to catch errors where
    different zone files have zone_id index mismatches, so we err on the side of explicitness

    with default 1-based contiguous zone ids, this fiel is optional and zone_ids can return None
    """
    table_settings = config.read_model_settings('tables.yaml')
    zone_id_file_name = table_settings.get('zone_ids')
    if not zone_id_file_name:
        return
    zone_ids_df = read_csv_file(data_dir, zone_id_file_name)
    zone_ids_df = zone_ids_df.rename(zone_aliases)
    assert 'zone' in zone_ids_df
    zone_ids_df.set_index('zone', drop=True, inplace=True, verify_integrity=True)
    assert zone_ids_df.index.is_monotonic_increasing
    tracing.write_csv(zone_ids_df, file_name='zone_ids',
      transpose=False)
    return zone_ids_df.index