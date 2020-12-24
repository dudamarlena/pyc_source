# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/conda/lib/python3.7/site-packages/QA_OTGBroker/__init__.py
# Compiled at: 2019-11-10 13:49:23
# Size of source mod 2**32: 19901 bytes
import websocket, json, QUANTAXIS as QA
from QA_OTGBroker.syscollect import get_system_info
try:
    import thread
except ImportError:
    import _thread as thread

import time

def send_order(account_cookie, order_direction='BUY', order_offset='OPEN', volume=1, order_id=False, code='rb1905', exchange_id='SHFE', price=3925, price_type='LIMIT', volume_condition='ANY', time_condition='GFD'):
    """[summary]

    Arguments:
        account_cookie {[type]} -- [description]

    Keyword Arguments:
        order_direction {str} -- [description] (default: {'BUY'})
        order_offset {str} -- [description] (default: {'OPEN'})
        volume {int} -- [description] (default: {1})
        order_id {bool} -- [description] (default: {False})
        code {str} -- [description] (default: {'rb1905'})
        exchange_id {str} -- [description] (default: {'SHFE'})

    Returns:
        [type] -- [description]
    """
    return json.dumps({'aid':'insert_order', 
     'user_id':account_cookie, 
     'order_id':order_id if order_id else QA.QA_util_random_with_topic('QAOTG'), 
     'exchange_id':exchange_id, 
     'instrument_id':code, 
     'direction':order_direction, 
     'offset':order_offset, 
     'volume':volume, 
     'price_type':price_type, 
     'limit_price':price, 
     'volume_condition':volume_condition, 
     'time_condition':time_condition})


def cancel_order(account_cookie, order_id):
    return json.dumps({'aid':'cancel_order', 
     'user_id':account_cookie, 
     'order_id':order_id})


def querybank(account_cookie, password, bankid, bankpassword):
    return json.dumps({'aid':'qry_bankcapital', 
     'bank_id':str(bankid), 
     'future_account':str(account_cookie), 
     'future_password':str(password), 
     'bank_password':str(bankpassword), 
     'currency':'CNY'})


def transfer(account_cookie, password, bankid, bankpassword, amount):
    return json.dumps({'aid':'req_transfer', 
     'future_account':str(account_cookie), 
     'future_password':str(password), 
     'bank_id':str(bankid), 
     'bank_password':str(bankpassword), 
     'currency':'CNY', 
     'amount':float(amount)})


def subscribe_quote(ins_list='SHFE.cu1612,CFFEX.IF1701'):
    return json.dumps({'aid':'subscribe_quote', 
     'ins_list':ins_list})


def peek():
    return json.dumps({'aid': 'peek_message'})


def login(name, password, broker, appid=''):
    """
    """
    login = {'aid':'req_login', 
     'bid':str(broker), 
     'user_name':str(name), 
     'password':str(password)}
    if appid:
        appid, systeminfo = get_system_info()
        login['client_app_id'] = appid
        login['client_system_info'] = systeminfo
    return json.dumps(login)


def query_settlement(day):
    return json.dumps({'aid':'qry_settlement_info', 
     'trading_day':day})


def change_password(old, new):
    return json.dumps({'aid':'change_password', 
     'old_password':str(old), 
     'new_password':str(new)})


def ping(ws):
    return ws.ping()


def parse_rtn(message):
    pass


class ORDER_TYPE:
    __doc__ = '        \n    Name\tValue/Description\n    TRADE\t交易指令\n    SWAP\t互换交易指令\n    EXECUTE\t期权行权指令\n    QUOTE\t期权询价指令'
    TRADE = 'TRADE'
    SWAP = 'SWAP'
    EXECUTE = 'EXECUTE'
    QUOTE = 'QUOTE'


def on_message(ws, message):
    QA.QA_util_log_info(message)


def on_ping(ws, message):
    print('ping')
    QA.QA_util_log_info(message)
    ws.pong(message)


def on_pong(ws, message):
    print('pong')
    QA.QA_util_log_info(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print('### closed ###')


def on_open(ws):

    def run(*args):
        acc1 = '131176'
        acc1_password = 'qchl123456'
        broker = 'simnow'
        login_1 = login(broker, acc1, acc1_password)
        QA.QA_util_log_info(login_1)
        ws.send(login_1)
        time.sleep(1)
        ws.send(peek())
        for i in range(100):
            ws.sock.ping('QUANTAXIS')
            time.sleep(1)

        time.sleep(20)
        ws.close()
        print('thread terminating...')

    thread.start_new_thread(run, ())