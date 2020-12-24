# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/resonate/compress.py
# Compiled at: 2019-02-13 12:17:39
# Size of source mod 2**32: 3853 bytes
import numpy as np, pandas as pd
from resonate.library.exceptions import GenericException

def compress_detections(detections, timefilter=3600):
    """
    Creates compressed dataframe from detection dataframe

    :param detections: detection dataframe
    :param timefilter: A maximum amount of time in seconds that can pass before
        a new detction event is started
    :return: A Pandas DataFrame matrix of detections events
    """
    if not isinstance(detections, pd.DataFrame):
        raise GenericException('input parameter must be a Pandas dataframe')
    mandatory_columns = set([
     'datecollected', 'catalognumber', 'unqdetecid', 'latitude', 'longitude'])
    if mandatory_columns.issubset(detections.columns):
        stations = detections.groupby('station').agg('mean')[['latitude', 'longitude']].reset_index()
        anm_list = detections['catalognumber'].unique()
        detections.sort_values([
         'catalognumber', 'datecollected'],
          inplace=True)
        detections['seq_num'] = np.nan
        anm_group = detections.groupby('catalognumber')
        out_df = pd.DataFrame()
        for catalognum in anm_list:
            a = anm_group.get_group(catalognum).copy(deep=True)
            a.sort_values(['datecollected', 'station'], inplace=True)
            a.datecollected = pd.to_datetime(a.datecollected)
            a['seq_num'] = ((a.station.shift(1) != a.station) | (a.datecollected.diff().dt.total_seconds() > timefilter)).astype(int).cumsum()
            out_df = out_df.append(a)

        stat_df = out_df.groupby(['catalognumber', 'seq_num']).agg({'datecollected':['min', 'max'],  'unqdetecid':[
          'first', 'last'], 
         'seq_num':'count'})
        stat_df.columns = ['_'.join(col).strip() for col in stat_df.columns.values]
        stat_df.datecollected_max = pd.to_datetime(stat_df.datecollected_max)
        stat_df.datecollected_min = pd.to_datetime(stat_df.datecollected_min)
        stat_df['avg_time_between_det'] = (stat_df['datecollected_max'] - stat_df['datecollected_min']) / np.maximum(1, stat_df['seq_num_count'] - 1)
        stat_df.rename(columns={'seq_num_count':'total_count',  'datecollected_max':'enddate',  'datecollected_min':'startdate', 
         'unqdetecid_first':'startunqdetecid',  'unqdetecid_last':'endunqdetecid'},
          inplace=True)
        stat_df.reset_index(inplace=True)
        out_df = out_df[['catalognumber', 'station', 'seq_num']].drop_duplicates().merge(stat_df,
          on=['catalognumber', 'seq_num'])
        out_df = out_df.merge(stations, on='station')
        return out_df
    raise GenericException('Missing required input columns: {}'.format(mandatory_columns - set(detections.columns)))