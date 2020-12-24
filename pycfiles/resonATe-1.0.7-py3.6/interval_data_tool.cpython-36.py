# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/resonate/interval_data_tool.py
# Compiled at: 2018-12-20 13:45:50
# Size of source mod 2**32: 3090 bytes
import geopy, pandas as pd

def interval_data(compressed_df, dist_matrix_df, station_radius_df=None):
    """
    Creates a detection interval file from a compressed detection, distance matrix and station detection radius DataFrames

    :param compressed_df: compressed detection dataframe
    :param dist_matrix_df: station distance matrix dataframe
    :param station_radius: station distance radius dataframe
    :return: interval detection Dataframe
    """
    fst = compressed_df[[
     'catalognumber', 'station', 'seq_num', 'total_count', 'startdate', 'enddate', 'endunqdetecid']].copy()
    snd = compressed_df[[
     'catalognumber', 'station', 'seq_num', 'total_count', 'startdate', 'enddate', 'endunqdetecid']].copy()
    snd.seq_num -= 1
    fst.columns = [
     'catalognumber', 'from_station', 'seq_num', 'from_detcnt',
     'from_arrive', 'from_leave', 'unqdetid_from']
    snd.columns = ['catalognumber', 'to_station', 'seq_num', 'to_detcnt',
     'to_arrive', 'to_leave', 'unqdetid_arrive']
    merged = pd.merge(fst, snd, how='left', on=['catalognumber', 'seq_num'])
    merged['intervaltime'] = None
    merged['intervalseconds'] = None
    merged['distance_m'] = None
    merged['metres_per_second'] = None
    for idx, item in merged.iterrows():
        if not (pd.isnull(item['from_station']) or pd.isnull(item['to_station'])):
            matrix_distance_m = dist_matrix_df.loc[(item['from_station'],
             item['to_station'])]
            if matrix_distance_m:
                if isinstance(station_radius_df, pd.DataFrame):
                    stn1_radius = station_radius_df.loc[(item['from_station'], 'radius')]
                    stn2_radius = station_radius_df.loc[(item['to_station'], 'radius')]
                    distance = max(geopy.distance.Distance(0).m, matrix_distance_m - stn1_radius.m - stn2_radius.m) * 1000
                else:
                    distance = max(geopy.distance.Distance(0).m, matrix_distance_m) * 1000
                merged.loc[(idx, 'distance_m')] = distance
                time_interval = item['to_arrive'] - item['from_leave']
                merged.loc[(idx, 'intervaltime')] = time_interval
                merged.loc[(idx, 'intervalseconds')] = time_interval.total_seconds()
                if time_interval.seconds != 0:
                    merged.loc[(idx, 'metres_per_second')] = distance / time_interval.seconds

    return merged