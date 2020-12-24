# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/posey/Documents/python-sdk/spawner/nlp.py
# Compiled at: 2020-04-20 15:54:42
# Size of source mod 2**32: 443 bytes
import requests, json, pandas as pd

def answer(question):
    url = 'https://spawnerapi.com/answer'
    trade_list = {'text': question}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, headers=headers, data=(json.dumps(trade_list)))
    content = r.text
    df = pd.read_json(content, orient='records')
    df = df.drop(columns=['chart_type', 'condensed_data'])
    return df