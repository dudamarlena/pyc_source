# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\DataGroup.py
# Compiled at: 2018-09-18 04:40:01
from lib.JsonClass import CJSON
import copy

class CDataGroup:

    def __init__(self, filepath):
        self.version = 'v1.0'
        objJSON = CJSON()
        self.temp = objJSON.loadfile(filepath)

    def add_group(self, name, comment, items):
        dc = {}
        dc['description'] = comment
        dc['name'] = name
        dc['version'] = 1
        dc['enable'] = False
        dc['items'] = self.add_items(items)
        self.temp['hisDataGroups'].append(dc)

    def add_items(self, items):
        lt = []
        for item in items:
            dc = {}
            dc['DataItems'] = {}
            dc['description'] = item['description']
            dc['name'] = item['name']
            dc['varType'] = item['varType']
            dc['version'] = 1
            dc['fixed'] = True
            dc['varData'] = ''
            lt.append(dc)

        return lt

    def output(self):
        objJSON = CJSON()
        return objJSON.outputjson(self.temp)