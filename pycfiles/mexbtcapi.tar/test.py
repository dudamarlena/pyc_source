# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: test.py
# Compiled at: 2012-09-29 11:45:53
import mexbtcapi
from mexbtcapi.concepts.currencies import USD
ten_dollars = mexbtcapi.concepts.currency.Amount(10, USD)
for api in mexbtcapi.apis:
    import pdb
    pdb.set_trace()
    print 'at', api.name, 'I can get', api.market(USD).getTicker().sell.convert(ten_dollars), 'for my', ten_dollars

key = '98b48666-6d56-4031-ea68-8ef0c6b3ddfe'
secret = 'A1dcxIWvAiTOhar4091KBoW5mo4ZNwu1QKNFdT3GfFplkYqy3PNbMLANJug0H54awun6dHfc6+QcMbLc7z7pUA=='
m = api.Market(USD)
t = m.getTicker()
print t.low
print t.high
print t.buy
print t.sell