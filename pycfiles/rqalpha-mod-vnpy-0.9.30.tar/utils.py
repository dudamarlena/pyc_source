# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-vnpy/rqalpha_mod_vnpy/utils.py
# Compiled at: 2017-05-22 05:50:22
from datetime import timedelta
import re
from rqalpha.environment import Environment
from rqalpha.const import POSITION_EFFECT, COMMISSION_TYPE

def make_underlying_symbol(id_or_symbol):
    return filter(lambda x: x not in '0123456789 ', id_or_symbol).upper()


def make_order_book_id(symbol):
    if len(symbol) < 4:
        return None
    else:
        if symbol[(-4)] not in '0123456789':
            order_book_id = symbol[:2] + '1' + symbol[-3:]
        else:
            order_book_id = symbol
        return order_book_id.upper()


def cal_commission(trade_dict, position_effect):
    order_book_id = trade_dict.order_book_id
    env = Environment.get_instance()
    info = env.data_proxy.get_commission_info(order_book_id)
    commission = 0
    if info['commission_type'] == COMMISSION_TYPE.BY_MONEY:
        contract_multiplier = env.get_instrument(trade_dict.order_book_id).contract_multiplier
        if position_effect == POSITION_EFFECT.OPEN:
            commission += trade_dict.price * trade_dict.amount * contract_multiplier * info['open_commission_ratio']
        elif position_effect == POSITION_EFFECT.CLOSE:
            commission += trade_dict.price * trade_dict.amount * contract_multiplier * info['close_commission_ratio']
        elif position_effect == POSITION_EFFECT.CLOSE_TODAY:
            commission += trade_dict.price * trade_dict.amount * contract_multiplier * info['close_commission_today_ratio']
    elif position_effect == POSITION_EFFECT.OPEN:
        commission += trade_dict.amount * info['open_commission_ratio']
    elif position_effect == POSITION_EFFECT.CLOSE:
        commission += trade_dict.amount * info['close_commission_ratio']
    elif position_effect == POSITION_EFFECT.CLOSE_TODAY:
        commission += trade_dict.amount * info['close_commission_today_ratio']
    return commission


def is_future(order_book_id):
    if order_book_id is None:
        return False
    else:
        return re.match('^[a-zA-Z]+[0-9]+$', order_book_id) is not None