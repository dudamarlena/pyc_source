# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/lib/fetchclimate/fc_request.py
# Compiled at: 2014-10-02 15:19:10
import datetime, json, re, requests
from fc_response import FCResponse

class FCRequest:

    def __init__(self, options=None):
        self.status = 'new'
        self.statusData = None
        self.dataSources = {}
        self.timeout = options['timeout'] if 'timeout' in options else 180000
        self.pollInterval = options['pollingInterval'] if 'pollingInterval' in options else 10000
        self.serviceUrl = options['serviceUrl'] if 'serviceUrl' in options else 'http://fetchclimate2.cloudapp.net'
        self.hash = ''
        if 'rawJSON' in options:
            self.requestJSON = options.rawJSON
        else:
            self.spatial = options['spatial']
            self.temporal = options['temporal']
            self.variable = options['variable']
            self.requestJSON = {'EnvironmentVariableName': str(self.variable), 
               'Domain': {'Mask': None}, 'ParticularDataSources': options['dataSources'] if 'dataSources' in options else [], 
               'ReproducibilityTimestamp': options['timestamp'] if 'timestamp' in options else 253404979199999}
            self.spatial.fillFetchRequest(self.requestJSON)
            self.temporal.fillFetchRequest(self.requestJSON)
        return

    def positionInQueue(self):
        if self.status != 'pending':
            return float('nan')
        return self.statusData

    def percentCompleted(self):
        if self.status == 'calculating':
            return self.statusData
        else:
            if self.status == 'receiving' or self.status == 'completed' or self.status == 'failed':
                return 100
            return 0

    def errorMessage(self):
        if self.status != 'failed':
            return ''
        return self.statusData

    def resultUrl(self):
        if self.status != 'completed':
            return None
        else:
            return self.statusData

    def onAjaxSuccess(self, answer):
        stat5 = answer[0:min(len(answer), 5)]
        print str(datetime.datetime.now()) + ': Status received ' + answer
        if stat5 == 'pendi' or stat5 == 'progr':
            hashIdx = answer.find('hash=')
            if hashIdx == -1:
                print 'No hash found in response: ' + answer
            else:
                self.hash = answer[hashIdx + 5:].strip()
            if stat5 == 'pendi':
                self.status = 'pending'
                self.statusData = int(re.findall('pending=(\\d+);', answer)[0])
            elif stat5 == 'progr':
                self.status = 'calculating'
                self.statusData = int(re.findall('progress=(\\d+)%;', answer)[0])
            return {'status': self.status, 'statusData': self.statusData}
        else:
            if stat5 == 'compl':
                self.status = 'receiving'
                self.statusData = answer[10:]
                hashIdx = answer.find('Blob=')
                if hashIdx != -1:
                    self.hash = answer[hashIdx + 5:].strip()
                return FCResponse(self, self.statusData)
            if stat5 == 'fault':
                hashIdx = answer.find('hash ')
                if hashIdx == -1:
                    print 'No hash found in response: ' + answer
                else:
                    self.hash = answer[hashIdx + 5:].strip()
                return
            return

    def doPost(self):
        self.status = 'pending'
        self.statusData = float('nan')
        headers = {'content-type': 'application/json; charset=utf-8', 'data-type': 'json'}
        r = requests.post(self.serviceUrl + '/api/compute', data=json.dumps(self.requestJSON), headers=headers, timeout=self.timeout)
        if r.status_code == requests.codes.ok:
            return self.onAjaxSuccess(r.json())
        return 'Error: ' + r.status_code

    def doStatusCheck(self):
        print str(datetime.datetime.now()) + ': Getting state for ' + self.hash
        r = requests.get(self.serviceUrl + '/api/status?hash=' + self.hash, timeout=self.timeout)
        if r.status_code == requests.codes.ok:
            return self.onAjaxSuccess(r.json())
        return 'Error: ' + r.status_code