# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/al_cloud_insight/__init__.py
# Compiled at: 2017-07-12 13:56:26
import logging
from hammock import Hammock
from tacoma import Tacoma
from cloud_explorer import CloudExplorer
from assets import Assets
from aims import AIMS

class CloudInsight(object):

    def __init__(self, username, password, host='https://api.cloudinsight.alertlogic.com', version='v1'):
        pre_auth_ci = Hammock(host, auth=(username, password))
        resp = pre_auth_ci.aims(version).authenticate.POST()
        logging.debug(resp.status_code)
        resp.raise_for_status()
        resp = resp.json()
        self.account_id = resp['authentication']['account']['id']
        self.auth_token = resp['authentication']['token']
        self.version = version
        headers = {'x-aims-auth-token': self.auth_token, 
           'Accept-encoding': 'gzip'}
        self.ci = Hammock(host, headers=headers)
        self.tacoma = Tacoma(self)
        self.cloud_explorer = CloudExplorer(self)
        self.assets = Assets(self)
        self.aims = AIMS(self)