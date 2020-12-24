# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blotter/util.py
# Compiled at: 2019-05-24 11:49:19
# Size of source mod 2**32: 332 bytes


def calc_pnl(qty1, px1, qty2, px2):
    """
    @returns float
    """
    qty = min(abs(qty2), abs(qty1))
    diff = px1 - px2 if qty2 > 0 else px2 - px1
    return qty * diff


def calc_avg_open_price(qty1, px1, qty2, px2):
    """
    @returns float
    """
    num = px1 * qty1 + px2 * qty2
    return num / (qty1 + qty2)