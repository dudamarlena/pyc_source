# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Code\Python\db_trans\zlshare\zlshare\vtrade\vtrade.py
# Compiled at: 2019-04-09 06:29:02
import urllib, urllib2, json, datetime, hashlib
API_HOST = 'http://web7.umydata.com'
PRI_KEY = 'Zealink25GiYmhM3PkJU9JN5ghu0EeVq'

class vtradectl(object):

    def __init__(self, user='', passwd='', api_host=API_HOST):
        self.api_host = api_host
        self.token = None
        self.user = user
        self.passwd = passwd
        return

    def _http_data(self, uri, postdata):
        requrl = self.api_host + uri
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = ('Basic {}').format(self.token)
        postdata_js = json.dumps(postdata)
        req = urllib2.Request(url=requrl, data=postdata_js, headers=headers)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def _get_sign(self, params):
        param = urllib.urlencode(params).encode('utf-8')
        param += ('&Key={}').format(PRI_KEY)
        sign = hashlib.md5(param).hexdigest()
        return sign.upper()

    def logon(self, user=None, passwd=None):
        self.user = user if user else self.user
        self.passwd = passwd if passwd else self.passwd
        md5passwd = hashlib.md5(self.passwd.encode('utf-8')).hexdigest()
        postdata = {'UserId': self.user, 
           'Password': md5passwd}
        postdata['Sign'] = self._get_sign(postdata)
        self.token = self._http_data('/api/VT_Logon', postdata=postdata)

    def buy(self, **params):
        u"""
        :param Symbol:  股票代码
        :param Name:    股票代码
        :param Price:    买入价格
        :param Vol:      买入笔数
        :param MaxCount:
        :param Policy:
        :return:
        """
        params['Sign'] = self._get_sign(params)
        return self._http_data('/api/VT_Buy', postdata=params)

    def sell(self, **params):
        u""""
        :param Symbol:  股票代码
        :param Name:    股票代码
        :param Price:    卖出价格
        :param Vol:      卖出笔数
        :param MaxCount:
        :param Policy:
        :return:
        """
        params['Sign'] = self._get_sign(params)
        return self._http_data('/api/VT_Sell', postdata=params)

    def cancel(self, bookid):
        postdata = {'BookId': bookid}
        postdata['Sign'] = self._get_sign(postdata)
        return self._http_data('/api/VT_Canel', postdata=postdata)

    def order(self, dtstart, dtend):
        u"""
        查询委托订单信息
        :param dtstart:
        :param dtend:
        :return:
        """
        postdata = {'QueryDate': {'StartDate': dtstart if isinstance(dtstart, str) else dtstart.strftime('%Y%m%d'), 
                         'EndDate': dtend if isinstance(dtend, str) else dtend.strftime('%Y%m%d')}, 
           'type': 0}
        postdata['Sign'] = self._get_sign(postdata)
        result = self._http_data('/api/VT_Query', postdata=postdata)
        return result['Entrust']

    def deal(self, dtstart, dtend):
        u"""
        查询成交信息
        :param dtstart:
        :param dtend:
        :return:
        """
        postdata = {'QueryDate': {'StartDate': dtstart if isinstance(dtstart, str) else dtstart.strftime('%Y%m%d'), 
                         'EndDate': dtend if isinstance(dtend, str) else dtend.strftime('%Y%m%d')}, 
           'type': 1}
        postdata['Sign'] = self._get_sign(postdata)
        result = self._http_data('/api/VT_Query', postdata=postdata)
        return result['deal']

    def info(self, stock=True):
        u"""
        查询持仓信息
        :param stock: 是否返回股票持仓信息
        :return:
        """
        postdata = {'stock': stock}
        postdata['Sign'] = self._get_sign(postdata)
        return self._http_data('/api/VT_User', postdata=postdata)