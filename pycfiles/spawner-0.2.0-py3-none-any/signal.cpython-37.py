# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/posey/Documents/python-sdk/spawner/signal.py
# Compiled at: 2020-04-17 17:52:56
# Size of source mod 2**32: 881 bytes
import requests, json

def fundamentals(token):
    url = 'https://spawnerapi.com/fundamentals/' + token
    response = requests.get(url)
    return response.json()


def sharpe(token, ticker, time_purchased):
    url = 'https://spawnerapi.com/sharpe/' + ticker + '/' + time_purchased + '/' + token
    response = requests.get(url)
    return response.text


def kelly_criterion(token, ticker):
    url = 'https://spawnerapi.com/kelly-criterion/' + ticker + '/' + token
    response = requests.get(url)
    return response.text


def limit_order(token, identifier, key, ticker, quantity, side, limit_price):
    url = 'https://spawnerapi.com/limit/' + identifier + '/' + key + '/' + ticker + '/' + quantity + '/' + side + '/' + limit_price + '/' + token
    response = requests.get(url)
    return response.text


class signals:

    def test(self):
        return 1