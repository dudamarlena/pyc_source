# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kipe/workspace/raspautomation_v2/cli/venv/lib/python2.7/site-packages/raspautomation_cli/device.py
# Compiled at: 2016-05-27 19:00:41


class Device(object):
    api_endpoint = None
    data = {}

    def __init__(self, server, data):
        self.server = server
        self.set_data(data)

    def get_data(self):
        self.data = self.server.get(self.endpoint).json()
        return self.data

    def set_data(self, data):
        self.data = data
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def endpoint(self):
        return self.api_endpoint + '/%i/' % self.id

    def to_json(self):
        return {key:value for key, value in self.__dict__.items() if key not in ('server',
                                                                                 'data') if key not in ('server',
                                                                                                        'data')}