# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/shinsheel/Documents/Data-Gathering/Pypi/anarcute/anarcute/predict.hy
# Compiled at: 2019-08-28 09:34:49
# Size of source mod 2**32: 920 bytes
import hy.macros, json, pandas as pd
from fbprophet import Prophet
import datetime
from anarcute import *
hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')

def predict_next(enumerated, n, all=False, values=thru, freq='MS', interval_width=0.95):
    ts = []
    for k, v in enumerated:
        ts.append({'ds':k,  'y':v})

    ts = pd.DataFrame.from_dict(ts)
    m = Prophet(interval_width=interval_width)
    m.fit(ts)
    future = m.make_future_dataframe(periods=n, freq=freq)
    prediction = m.predict(future)
    prediction = lambda hyx_Xpercent_signX1:     if all:
hyx_Xpercent_signX1 # Avoid dead code: hyx_Xpercent_signX1[slice(-1 * n, None)](list(prediction[['ds', 'yhat']].as_matrix()))
    for row in prediction:
        row[0] = row[0].strftime('%Y-%m-%d')
        row[-1] = round(values(row[(-1)]), 2)

    prediction = prediction
    return lambda arr: list(map(list, arr))(prediction)