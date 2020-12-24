# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/goapi.py
# Compiled at: 2011-10-05 02:42:28
try:
    import simplejson as json
except:
    from django.utils import simplejson as json

import goristock, realtime, twseno
from gnews import gnews

class goapi(object):

    def __init__(self, stock_no):
        self.stock_no = stock_no

    @property
    def stock_j(self):
        try:
            stock = goristock.goristock(self.stock_no)
            re = {'stock_name': stock.stock_name, 
               'stock_no': stock.stock_no, 
               'stock_date': stock.data_date[(-1)], 
               'stock_price': stock.raw_data[(-1)], 
               'stock_range': stock.stock_range[(-1)], 
               'stock_range_per': stock.range_per, 
               'stock_vol': stock.stock_vol[(-1)] / 1000, 
               'stock_open': stock.stock_open[(-1)], 
               'stock_h': stock.stock_h[(-1)], 
               'stock_l': stock.stock_l[(-1)], 
               'RABC': stock.RABC}
        except:
            re = {'ERRORREPORT': "Can't fetch stock data."}

        return json.dumps(re, ensure_ascii=False)

    @property
    def stock_real(self):
        try:
            re = realtime.twsk(self.stock_no).real
        except:
            re = {'ERRORREPORT': "Can't fetch real stock data."}

        return json.dumps(re, ensure_ascii=False)


def weight():
    try:
        re = realtime.twsew().weight
    except:
        re = {'ERRORREPORT': "Can't fetch weight data."}

    return json.dumps(re, ensure_ascii=False)


def stocklist():
    stock_list = twseno.twseno().allstockno
    re_st = {}
    for i in stock_list:
        re_st.update({i: stock_list[i].decode('utf-8')})

    re = {'stocklist': re_st, 'n': len(stock_list)}
    re.update({'last_update': twseno.twseno().last_update})
    return json.dumps(re, ensure_ascii=False)


def searchstock(q):
    q = q.encode('utf-8').replace(' ', '')
    if q:
        rq = twseno.twseno().search(q)
        re_se = {}
        for i in rq:
            re_se.update({i: rq[i].decode('utf-8')})

        re = {'result': re_se, 'n': len(rq)}
        return json.dumps(re, ensure_ascii=False)
    else:
        re = {'ERRORREPORT': 'No keyword.'}
        return json.dumps(re, ensure_ascii=False)


def newsapi(q=None, rsz=8):
    try:
        if q:
            q = q.encode('utf-8')
            n = gnews(q, rsz=rsz).formatre
        else:
            n = gnews('', 'b', rsz).formatre
        return json.dumps(n, ensure_ascii=False)
    except TypeError:
        re = {'ERRORREPORT': 'No result.'}
        return json.dumps(re, ensure_ascii=False)