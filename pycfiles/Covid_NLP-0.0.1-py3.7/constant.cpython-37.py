# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/covid_nlp/constant.py
# Compiled at: 2020-03-10 06:33:50
# Size of source mod 2**32: 1740 bytes
import os, pathlib
from enum import Enum
import tensorflow as tf, tensorflow_hub as hub, numpy as np, tensorflow_text, pandas as pd

class Urls:
    CONFIRMED = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    DEATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    RECOVERY = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
    USE = 'https://tfhub.dev/google/universal-sentence-encoder-qa/3'


module = hub.load(Urls.USE)
data_path = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv((os.path.join(data_path, 'data.csv')), delimiter=',')
response = df['Response'].values
context = df['Context'].values
response_embeddings = module.signatures['response_encoder'](input=(tf.constant(response)),
  context=(tf.constant(context)))
confirmed_df = pd.read_csv(Urls.CONFIRMED)
death_df = pd.read_csv(Urls.DEATH)
recovery_df = pd.read_csv(Urls.RECOVERY)
cols = confirmed_df.keys()
all_confirmed = confirmed_df.loc[:, cols[4]:cols[(-1)]]
all_deaths = death_df.loc[:, cols[4]:cols[(-1)]]
all_recoveries = recovery_df.loc[:, cols[4]:cols[(-1)]]
dates = all_confirmed.keys()
latest_confirmed = confirmed_df[dates[(-1)]]
latest_deaths = death_df[dates[(-1)]]
latest_recoveries = recovery_df[dates[(-1)]]
unique_countries = list(confirmed_df['Country/Region'].unique())