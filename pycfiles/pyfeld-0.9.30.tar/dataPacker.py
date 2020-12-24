# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/dataPacker.py
# Compiled at: 2017-11-23 08:41:51


class DataPacker:

    @staticmethod
    def dataTypeList():
        return 'list'

    @staticmethod
    def dataTypeObject():
        return 'object'

    def __init__(self, type):
        self.type = type
        self.data = []

    def add_pair(self, key, value):
        self.data.append([key, value])

    def add_value(self, key, value):
        self.data.append(key, value)

    def to_string(self, coding):
        if self.type == self.dataTypeObject():
            if coding == 'json':
                s = '{'
                for item in self.data:
                    s += ' "' + item[0] + '": '
                    s += '"' + item[1] + '"\n'

                s += '}'
            else:
                for item in self.data:
                    s += item[0].replace('=', '\\=') + '='
                    s += item[1] + '\n'

        if self.type == self.dataTypeList():
            if coding == 'json':
                s = '['
                for item in self.data:
                    s += '"' + item[1] + '"\n'

                s += ']'
            else:
                for item in self.data:
                    s += item[1] + '\n'

        return s