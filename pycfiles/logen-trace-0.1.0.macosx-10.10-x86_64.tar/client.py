# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/py/.pyenv/versions/logen-trace/lib/python2.7/site-packages/logen/client.py
# Compiled at: 2015-12-17 00:41:55
from datetime import datetime
from pytz import timezone
from suds.client import Client

class Logen(object):

    def __init__(self, logen_id, logen_password, logen_url='http://ilogen.ilogen.com/iLOGEN.EDI.WebService/W_PHPServer.asmx?WSDL', current_tz=timezone('Asia/Seoul')):
        self.logen_id = logen_id
        self.logen_password = logen_password
        self.client = Client(logen_url)
        self.current_tz = current_tz

    def get_datetime(self, date_string, time_string):
        dt = datetime.strptime((' ').join([date_string, time_string]), '%Y%m%d %H%M%S')
        local = self.current_tz.localize(dt)
        return local

    def get_array(self, text):
        text = text.replace('〓', '')
        result = []
        for row in text.split('≡'):
            td = row.split('Ξ')
            if td.__len__() < 4:
                continue
            result.append({'invoice': td[0], 
               'datetime': self.get_datetime(td[1], td[2]), 
               'status': td[3]})

        return result

    def trace(self, invoices):
        res = self.client.service.W_PHP_NTx_Get_Trace_M(self.logen_id, self.logen_password, ("'{}'").format(("','").join(invoices)))
        result = []
        for row in self.get_array(res):
            status = row.get('status')
            if status == '배송완료':
                result.append((row.get('invoice'), row.get('datetime')))

        return result