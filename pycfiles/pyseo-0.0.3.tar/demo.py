# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysentosa/demo.py
# Compiled at: 2016-03-13 09:01:11
__author__ = 'Wu Fuheng(henry.woo@outlook.com)'
__version__ = '0.1.32'

def run_demo():
    s = "from pysentosa import Merlion\nfrom ticktype import *\n\nm = Merlion()\ntarget = 'SPY'\nm.track_symbol([target, 'BITA'])\nbounds = {target: [220, 250]}\nwhile True:\n  symbol, ticktype, value = m.get_mkdata()\n  if symbol == target:\n    if ticktype == ASK_PRICE and value < bounds[symbol][0]:\n        oid = m.buy(symbol, 5)\n        while True:\n            ord_st = m.get_order_status(oid)\n            print ORDSTATUS[ord_st]\n            if ord_st == FILLED:\n                bounds[symbol][0] -= 20\n                break\n            sleep(2)\n    elif ticktype == BID_PRICE and value > bounds[symbol][1]:\n        oid = m.sell(symbol, 100)\n        bounds[symbol][1] += 20"
    print '*' * 80
    print s
    print '*' * 80
    exec s


if __name__ == '__main__':
    run_demo()