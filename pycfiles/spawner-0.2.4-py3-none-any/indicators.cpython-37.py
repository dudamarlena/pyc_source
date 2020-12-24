# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/posey/Documents/python-sdk/spawner/indicators.py
# Compiled at: 2020-04-19 19:26:31
# Size of source mod 2**32: 1065 bytes
import requests, json, pandas

def health(token, ticker):
    url = 'https://spawnerapi.com/health/' + ticker + '/' + token
    response = requests.get(url).json()
    return response


def fundamentals(token):
    url = 'https://spawnerapi.com/fundamentals/' + token
    response = requests.get(url).json()
    return response.read_json()


def macro(token):
    url = 'https://spawnerapi.com/macro/' + token
    response = requests.get(url).json()
    return response


def rsi(token, ticker):
    url = 'https://spawnerapi.com/rsi/' + token
    response = requests.get(url).json()
    return response


def stochastic(token, ticker):
    url = 'https://spawnerapi.com/stochastic/' + token
    response = requests.get(url).json()
    return response


def kaufman(token):
    url = 'https://spawnerapi.com/kaufman/' + token
    response = requests.get(url).json()
    return response


def momentum(token):
    url = 'https://spawnerapi.com/momentum/' + ticker + '/' + token
    response = requests.get(url).text
    return response