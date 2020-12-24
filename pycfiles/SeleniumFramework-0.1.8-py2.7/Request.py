# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Request.py
# Compiled at: 2018-04-07 15:45:25
import requests, json

class Request:
    data = object

    def __init__(self, parsm_data):
        self.data = parsm_data

    def post(self):
        response = requests.post(self.data['endpoint'], headers=self.data['headers'], data=json.dumps(self.data['body']))
        return response

    def get(self):
        response = requests.get(self.data['endpoint'], headers=self.data['headers'], params=self.data['body'])
        return response

    def put(self):
        response = requests.put(self.data['endpoint'], headers=self.data['headers'], data=json.dumps(self.data['body']))
        return response

    def delete(self):
        response = requests.delete(self.data['endpoint'], headers=self.data['headers'], params=self.data['body'])
        return response