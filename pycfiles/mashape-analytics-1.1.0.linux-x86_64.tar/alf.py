# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/.virtualenvs/mashape-test/lib/python2.7/site-packages/mashapeanalytics/alf.py
# Compiled at: 2016-05-16 16:57:56
import json, six

@six.python_2_unicode_compatible
class Alf(object):
    """
  API Logging Format (ALF) Object
  """

    def __init__(self, serviceToken, environment, clientIp=None):
        self.serviceToken = serviceToken
        self.environment = environment
        self.clientIp = clientIp
        self.entries = []

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        alf = {'version': '1.0.0', 
           'serviceToken': self.serviceToken, 
           'environment': self.environment, 
           'har': {'log': {'version': '1.2', 
                           'creator': {'name': 'mashape-analytics-agent-python', 
                                       'version': '1.1.0'}, 
                           'entries': self.entries}}}
        if self.clientIp:
            alf['clientIPAddress'] = self.clientIp
        return alf

    @property
    def json(self):
        return self.to_json()

    def addEntry(self, entry):
        self.entries.append(entry)