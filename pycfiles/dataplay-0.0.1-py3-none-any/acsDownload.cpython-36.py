# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /content/drive/My Drive/colabs/dataplay/dataplay/acsDownload.py
# Compiled at: 2020-03-17 21:48:52
# Size of source mod 2**32: 8692 bytes
__all__ = [
 'retrieve_acs_data']
import ipywidgets as widgets
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import urllib.request
from urllib.parse import urlencode
import socket
socket.setdefaulttimeout(10.0)
import pandas as pd
pd.set_option('display.max_colwidth', -1)
import json, numpy as np
from pandas.io.json import json_normalize
import csv, geopandas as gpd
from geopandas import GeoDataFrame
import psycopg2, pandas, numpy
from shapely import wkb
from shapely.wkt import loads
import os, sys, fiona
fiona.drvsupport.supported_drivers['kml'] = 'rw'
fiona.drvsupport.supported_drivers['KML'] = 'rw'
import matplotlib.pyplot as plt, glob, imageio

def retrieve_acs_data(state, county, tract, tableId, year, saveAcs):
    dictionary = ''
    keys = []
    vals = []
    header = []
    keys1 = keys2 = keys3 = keys4 = keys5 = keys6 = keys7 = keys8 = ''
    keyCount = 0

    def getParams(keys):
        return {'get':'NAME' + keys, 
         'for':'tract:' + tract, 
         'in':'state:' + state + ' county:' + county, 
         'key':'829bf6f2e037372acbba32ba5731647c5127fdb0'}

    def getCityParams(keys):
        return {'get':'NAME' + keys, 
         'for':'county:' + county, 
         'in':'state:' + state, 
         'key':'829bf6f2e037372acbba32ba5731647c5127fdb0'}

    def readIn(url):
        tbl = pd.read_json(url, orient='records')
        tbl.columns = tbl.iloc[0]
        return tbl

    def addKeys(table, params):
        table2 = readIn(base + urlencode(getParams(params)))
        table3 = readIn(base + urlencode(getCityParams(params)))
        table3['tract'] = '010000'
        table2.append([table2, table3], sort=False)
        table2 = pd.concat([table2, table3], ignore_index=True)
        table = pd.merge(table, table2, how='left', left_on=[
         'NAME', 'state', 'county', 'tract'],
          right_on=[
         'NAME', 'state', 'county', 'tract'])
        return table

    url = 'https://api.census.gov/data/20' + year + '/acs/acs5/groups/' + tableId + '.json'
    metaDataTable = pd.read_json(url, orient='records')
    for key in metaDataTable['variables'].keys():
        if key[-1:] == 'E':
            keyCount = keyCount + 1
            if keyCount < 40:
                keys1 = keys1 + ',' + key
            else:
                if keyCount < 80:
                    keys2 = keys2 + ',' + key
                else:
                    if keyCount < 120:
                        keys3 = keys3 + ',' + key
                    else:
                        if keyCount < 160:
                            keys4 = keys4 + ',' + key
                        else:
                            if keyCount < 200:
                                keys5 = keys5 + ',' + key
                            else:
                                if keyCount < 240:
                                    keys6 = keys6 + ',' + key
                                else:
                                    if keyCount < 280:
                                        keys7 = keys7 + ',' + key
                                    else:
                                        if keyCount < 320:
                                            keys8 = keys8 + ',' + key
            keys.append(key)
            val = metaDataTable['variables'][key]['label']
            val = key + '_' + val.replace('Estimate!!', '').replace('!!', '_').replace(' ', '_')
            vals.append(val)

    dictionary = dict(zip(keys, vals))
    url1 = 'https://api.census.gov/data/20' + year + '/acs/acs5?'
    url2 = 'https://api.census.gov/data/20' + year + '/acs/acs5/subject?'
    base = ''
    if tableId[:1] == 'B':
        base = url1
    if tableId[:1] == 'S':
        base = url2
    url = base + urlencode(getParams(keys1))
    table = pd.read_json(url, orient='records')
    table.columns = table.iloc[0]
    table = table.iloc[1:]
    url = base + urlencode(getCityParams(keys1))
    table2 = pd.read_json(url, orient='records')
    table2.columns = table2.iloc[0]
    table2 = table2[1:]
    table2['tract'] = '010000'
    table.append([table, table2], sort=False)
    table = pd.concat([table, table2], ignore_index=True)
    if keys2 != '':
        table = addKeys(table, keys2)
    if keys3 != '':
        table = addKeys(table, keys3)
    if keys4 != '':
        table = addKeys(table, keys4)
    if keys5 != '':
        table = addKeys(table, keys5)
    if keys6 != '':
        table = addKeys(table, keys6)
    if keys7 != '':
        table = addKeys(table, keys7)
    if keys8 != '':
        table = addKeys(table, keys8)
    print('Number of Columns', len(dictionary))
    header = []
    for column in table.columns:
        if column in keys:
            header.append(dictionary[column])
        else:
            header.append(column)

    table.columns = header
    table['NAME'] = table['NAME'].str.replace(', Baltimore city, Maryland', '')
    table['NAME'][table['NAME'] == 'Baltimore city, Maryland'] = 'Baltimore City'
    table = table.apply((pd.to_numeric), errors='ignore')
    table.set_index('NAME', inplace=True)
    if saveAcs:
        table.to_csv(('./' + state + county + '_' + tableId + '_5y' + year + '_est_Original.csv'), quoting=(csv.QUOTE_ALL))
        saveThis = table.rename(columns=(lambda x: str(x)[:] if str(x) in ('NAME', 'state', 'county', 'tract') else str(x)[12:]))
        saveThis.to_csv(('./' + state + county + '_' + tableId + '_5y' + year + '_est.csv'), quoting=(csv.QUOTE_ALL))
    return table