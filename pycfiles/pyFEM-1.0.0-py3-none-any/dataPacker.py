# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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