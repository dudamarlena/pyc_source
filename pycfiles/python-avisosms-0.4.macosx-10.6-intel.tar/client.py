# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/avisosms/client.py
# Compiled at: 2014-01-30 04:26:18
from __future__ import unicode_literals
import json, requests
from avisosms.base import MountPoint
from avisosms.plugins import SendSMSPlugin, BalancePlugin, MobileCommercePlugin, TelephoneBookPlugin, RARPlugin

class BaseAvisoSMSClient(object):
    BASE_URL = b'http://api.avisosms.ru'
    __metaclass__ = MountPoint

    def __init__(self, username, password):
        super(BaseAvisoSMSClient, self).__init__()
        self.username = username
        self.password = password

    def post_json(self, data, url):
        headers = {b'Content-type': b'application/json', b'Accept': b'text/plain', b'charset': b'utf8'}
        r = requests.post(url=self.BASE_URL + url, data=json.dumps(data), headers=headers)
        return r.json()


class AvisoSMSClient(BaseAvisoSMSClient):
    plugins = (
     SendSMSPlugin, BalancePlugin, MobileCommercePlugin, TelephoneBookPlugin, RARPlugin)

    def __init__(self, username, password, service_id=None, secure_hash=None):
        super(AvisoSMSClient, self).__init__(username, password)
        self.service_id = service_id
        self.secure_hash = secure_hash