# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/posey/Documents/python-sdk/spawner/metrics.py
# Compiled at: 2020-04-20 15:54:49
# Size of source mod 2**32: 822 bytes
import requests, json, pandas

def sharpe(token, ticker, date):
    url = 'https://spawnerapi.com/sharpe/' + ticker + '/' + date + '/' + token
    response = requests.get(url).text
    return round(float(response), 2)


def volatility(token, ticker, date):
    url = 'https://spawnerapi.com/volatility/' + ticker + '/' + date + '/' + token
    response = requests.get(url).text
    return round(float(response), 2)


def expected_return(token, ticker, date):
    url = 'https://spawnerapi.com/expected-return/' + ticker + '/' + date + '/' + token
    response = requests.get(url).text
    return round(float(response), 2)


def kelly_criterion(token, ticker):
    url = 'https://spawnerapi.com/kelly-criterion/' + ticker + '/' + token
    response = requests.get(url).text
    return round(float(response), 2)