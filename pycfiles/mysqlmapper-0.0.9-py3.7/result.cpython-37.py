# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\result\result.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1405 bytes
import json
from datetime import datetime

class CodeModeDTO:
    code = 0
    message = ''
    data = {}

    def __init__(self, code, message, data):
        """
        Initialization status transfer tool class
        :param code: Status code
        :param message: Message body
        :param data: Data volume
        """
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        """
        Convert to JSON object
        :return:
        """
        self.data = self._parse_time(self.data)
        return json.dumps({'code':self.code, 
         'message':self.message, 
         'data':self.data})

    def _parse_time(self, data):
        """
        Recursive processing time format
        :param data: Data to be processed
        :return: Processing result
        """
        if isinstance(data, datetime):
            data = data.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(data, tuple) or isinstance(data, list):
            for i in range(0, len(data)):
                data[i] = self._parse_time(data[i])

        if isinstance(data, dict):
            for key in data.keys():
                data[key] = self._parse_time(data[key])

        return data