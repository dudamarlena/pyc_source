# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/output.py
# Compiled at: 2019-09-30 09:22:13
# Size of source mod 2**32: 1893 bytes
from .base import Base

class Output(Base):

    def __init__(self, api):
        super(Output, self).__init__(api)
        self.api = api

    def get_predictions(self, machine, label, start, end=None):
        params = dict(machine=machine,
          label=label)
        params['from'] = start
        if end is not None:
            params['to'] = end
        endpoint = '/predictions'
        return self.api.GET(endpoint, params=params)

    def get_evaluations(self, machine, label, start=None, end=None, execution_id=None):
        params = dict(machine=machine,
          label=label)
        if execution_id is not None:
            params['execution_id'] = execution_id
        if start is not None:
            params['from'] = start
        if end is not None:
            params['to'] = end
        endpoint = '/evaluations'
        return self.api.GET(endpoint, params=params)

    def get_scores(self, machine, label, start=None, end=None, execution_id=None):
        params = dict(machine=machine,
          label=label)
        if execution_id is not None:
            params['execution_id'] = execution_id
        if start is not None:
            params['from'] = start
        if end is not None:
            params['to'] = end
        endpoint = '/scores'
        return self.api.GET(endpoint, params=params)

    def get_features(self, machine, label, start=None, end=None, execution_id=None):
        params = dict(machine=machine,
          label=label)
        if execution_id is not None:
            params['execution_id'] = execution_id
        if start is not None:
            params['from'] = start
        if end is not None:
            params['to'] = end
        endpoint = '/features'
        return self.api.GET(endpoint, params=params)