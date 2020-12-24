# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../src/sam_simulation.py
# Compiled at: 2018-01-22 02:23:47
# Size of source mod 2**32: 11469 bytes
"""
Solar database
Example:
    Example of usage goes here

Attributes:
    module_level_variabless: None for the moment
Todo:
    * Implement multiple inputs and outputs for LCOE.
    * Clean code
"""
from __future__ import division, print_function
import sys, numpy as np, os
sys.path.append('.')
import tqdm, pandas as pd, sscapi, solar
raw_path = '../data/raw/'
folder_name = 'NSRDB/'
data_path = raw_path + folder_name

def _create_data_folder(path, year):
    """ Create data folder
    
    Args:
        path (str): os.path of folder
        year (str): Year of the data to be downloaded

    Returns:
        bool: True
    
    """
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    else:
        if not os.path.exists(data_path + year + '/timeseries/'):
            os.makedirs(data_path + year + '/timeseries/')
        if not os.path.exists(data_path + year + '/meta/'):
            os.makedirs(data_path + year + '/meta/')
    return True


def get_solar_data(path=data_path, filename='solar_example.csv', tmy=False, **kwargs):
    """ Read solar data from data_path
        
        Read csv file and modify the custom index by a DateTimeIndex using 
        columns ['Year', 'Month', 'Day', 'Hour', 'Minute']
    
    Args:
        path (str): data folder direction
        filename (str): data filename inside the data folder
        tmy (str): tmy data type
        
    Returns
        pd.DataFrame: data with modified index
    """
    data = pd.read_csv((path + filename + '.csv'), index_col=0)
    if 'tmy' not in path:
        try:
            data.index = pd.to_datetime(data[['Year', 'Month', 'Day', 'Hour',
             'Minute']])
        except TypeError:
            data.index = pd.to_datetime(data.index)

        data = data.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'], axis=1)
    else:
        data.index = pd.to_datetime(data[['Year', 'Month', 'Day', 'Hour',
         'Minute']])
        data = data.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'], axis=1)
    return data


def get_nsrdb_data(lat, lon, year, filename=None, path=data_path, force_download=False, timeseries=True, meta=False, **kwargs):
    """ Get the solar radiation data
    
    
    Args:
        lat (float): Latitude of the place
        lon (float): Longitude of the place
        year (str): String of the year in the format '2017/'
        filename (str): Filename of the data to be downloaded
        path (str): Data path
        force_download (bool): Force download data
        timeseries (bool): Output radiation timeseries
        meta (bool): Output radiation metadata
        

    Returns:
        bool: Description of return value
    
    """
    _create_data_folder(path, year)
    if not filename:
        filename = '{0}_{1}.csv'.format(lat, lon)
    else:
        if force_download or not os.path.exists(path + year + '/timeseries/' + filename + '.csv'):
            _ = _nsrdb_data(lon, lat, year, path=path, filename=filename, **kwargs)
            if isinstance(_, pd.DataFrame):
                print('dumb')
            else:
                print('Data download failed')
                sys.exit(1)
        else:
            print('Data created in {0}'.format(path + year + filename))
    if meta:
        meta = pd.read_csv(path + year + '/meta/' + filename + '.csv')
        return meta
    else:
        if timeseries:
            time_series_path = path + year + '/timeseries/'
            data = get_solar_data(path=time_series_path, filename=filename)
            return data
        return True


def check_nsrdcb(data):
    """ NSRDB FIX
    This function is to fix a bug that prevent to use sam.

    07/25/2017: BUG1 if DHI or any irradiation is negative the code fails.
        Temporal fix: Change negative values to 0
    """
    data = data[data['DHI'] < 0] = 0
    return data


def _nsrdb_data(lon, lat, year, path, filename, **kwargs):
    """ NRSDB API 
    
    Request to the radiation data from the NSRDB API. Default columns requested.
    If needed more columns a modification to attributes variables is needed.
    
    Args:
        lon (float): longitude in degrees
        lat (float): latitude in degrees
        year (str): year in str format with a backslash at the end (2017/)
        path (str): data path
        filename (str): filename of data
        kwargs (dict): Dictionary with api_key to request data 
    Returns
        pd.DataFrame: Solar radiation Time series
    """
    api_key = kwargs['api_key']
    if not year == 'tmy':
        attributes = 'ghi,dhi,dni,wind_speed_10m_nwp,surface_air_temperature_nwp,solar_zenith_angle'
    else:
        print('tmy attributes')
        attributes = 'ghi,dhi,dni,wind_speed_10m_nwp,surface_air_temperature_nwp'
    leap_year = 'false'
    interval = '60'
    utc = 'false'
    your_name = 'Pedro+Sanchez'
    reason_for_use = 'Research'
    your_affiliation = 'IER+UNAM'
    your_email = 'pesap@ier.unam.mx'
    mailing_list = 'false'
    url = 'http://developer.nrel.gov/api/solar/nsrdb_0512_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    df = pd.read_csv(url, header=None, index_col=[0])
    meta = df[:2].reset_index().copy()
    meta = meta.rename(columns=(meta.iloc[0])).drop(0)
    meta.to_csv(path + year + '/meta/' + filename + '.csv')
    time_series = df[2:].dropna(axis=1).reset_index().copy()
    time_series = time_series.rename(columns=(time_series.iloc[0])).drop(0)
    time_series.to_csv(path + year + '/timeseries/' + filename + '.csv')
    return time_series


def performance_simulation(meteo_data, *args, **kwargs):
    """ SAM performance simulation
    
    Perform a PVWATTS simulation using the SAM python implementation.
    
    Args:
        meteo_data (pd.DataFrame): Solar radiation dataframe
        kwargs (dictionary): Dictionary containing simulation parameters
        
    Returns:
        CP (float): Capacity factor
        Generation (float): Generation over the year of simulation
        meto_data (pd.DataFrame): Dataframe with hourly generation
    
    """
    params = {'lat':kwargs['lat'], 
     'lon':kwargs['lon'], 
     'timezone':kwargs['timezone'], 
     'elevation':kwargs['elevation'], 
     'sys_capacity':kwargs['system_capacity'], 
     'dc_ac_ratio':kwargs['dc_ac_ratio'], 
     'inv_eff':kwargs['inv_eff'], 
     'losses':kwargs['losses'], 
     'configuration':kwargs['configuration'], 
     'tilt':kwargs['tilt']}
    ssc = sscapi.PySSC()
    wfd = ssc.data_create()
    ssc.data_set_number(wfd, 'lat', params['lat'])
    ssc.data_set_number(wfd, 'lon', params['lon'])
    ssc.data_set_number(wfd, 'tz', params['timezone'])
    ssc.data_set_number(wfd, 'elev', params['elevation'])
    ssc.data_set_array(wfd, 'year', meteo_data.index.year)
    ssc.data_set_array(wfd, 'month', meteo_data.index.month)
    ssc.data_set_array(wfd, 'day', meteo_data.index.day)
    ssc.data_set_array(wfd, 'hour', meteo_data.index.hour)
    ssc.data_set_array(wfd, 'minute', meteo_data.index.minute)
    ssc.data_set_array(wfd, 'dn', meteo_data['DNI'])
    ssc.data_set_array(wfd, 'df', meteo_data['DHI'])
    ssc.data_set_array(wfd, 'wspd', meteo_data['Wind Speed'])
    ssc.data_set_array(wfd, 'tdry', meteo_data['Temperature'])
    dat = ssc.data_create()
    ssc.data_set_table(dat, 'solar_resource_data', wfd)
    ssc.data_free(wfd)
    ssc.data_set_number(dat, 'system_capacity', params['sys_capacity'])
    ssc.data_set_number(dat, 'dc_ac_ratio', params['dc_ac_ratio'])
    ssc.data_set_number(dat, 'tilt', params['tilt'])
    ssc.data_set_number(dat, 'azimuth', 180)
    ssc.data_set_number(dat, 'inv_eff', params['inv_eff'])
    ssc.data_set_number(dat, 'losses', params['losses'])
    ssc.data_set_number(dat, 'gcr', 0.4)
    ssc.data_set_number(dat, 'adjust:constant', 0)
    system_capacity = params['sys_capacity']
    value = params['configuration']
    if isinstance(params['configuration'], dict):
        d = {}
        for key, val in value.iteritems():
            ssc.data_set_number(dat, 'array_type', val)
            mod = ssc.module_create('pvwattsv5')
            ssc.module_exec(mod, dat)
            meteo_data['generation'] = np.array(ssc.data_get_array(dat, 'gen'))
            CP = meteo_data['generation'].sum() / (525600 / int('60') * system_capacity)
            generation = meteo_data['generation'].sum()
            d[key] = CP
            d['gen_' + key] = generation

        ssc.data_free(dat)
        ssc.module_free(mod)
        return d
    else:
        ssc.data_set_number(dat, 'array_type', value)
        mod = ssc.module_create('pvwattsv5')
        ssc.module_exec(mod, dat)
        meteo_data['generation'] = np.array(ssc.data_get_array(dat, 'gen'))
        CP = meteo_data['generation'].sum() / (525600 / int('60') * system_capacity)
        generation = meteo_data['generation'].sum()
        ssc.data_free(dat)
        ssc.module_free(mod)
        return (CP, generation, meteo_data)
        return True