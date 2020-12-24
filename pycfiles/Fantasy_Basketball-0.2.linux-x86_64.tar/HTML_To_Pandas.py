# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/HTML_To_Pandas.py
# Compiled at: 2014-10-14 21:34:25
__author__ = 'Devin Kelly'
import copy, pycurl, cStringIO, re, os, matplotlib.pyplot as plt, pandas as pd, numpy as np
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', None)
pd.set_option('display.precision', 4)
htmlRoot = 'html/'
minimumMinutesPlayed = 200
data_dir = 'html_data'

def htmlToPandas(filename, name):
    cols = [
     'Season', 'Lg', 'Team', 'W', 'L', 'W/L%', 'Finish', 'SRS', 'Pace',
     'Rel_Pace', 'ORtg', 'Rel_ORtg', 'DRtg', 'Rel_DRtg', 'Playoffs',
     'Coaches', 'WS']
    df = get_dataframe(filename, name)
    df.columns = cols
    df['WS'].replace('\\xc2\\xa0', value=' ', inplace=True, regex=True)
    df['Team'] = name
    df['Season'].replace('-\\d\\d$', value='', inplace=True, regex=True)
    df['Season'] = df['Season'].astype(int)
    df['W'] = df['W'].astype(int)
    df['L'] = df['L'].astype(int)
    df['W/L%'] = df['W/L%'].astype(float)
    df['Finish'] = df['Finish'].astype(float)
    df['SRS'] = df['SRS'].astype(float)
    df['Pace'] = df['Pace'].astype(float)
    df['Rel_Pace'] = df['Rel_Pace'].astype(float)
    df['ORtg'] = df['ORtg'].astype(float)
    df['Rel_ORtg'] = df['Rel_ORtg'].astype(float)
    df['DRtg'] = df['DRtg'].astype(float)
    df['Rel_DRtg'] = df['Rel_DRtg'].astype(float)
    with open('tmp.html', 'w') as (fd):
        fd.write(df.to_html().encode('utf-8'))
    return df