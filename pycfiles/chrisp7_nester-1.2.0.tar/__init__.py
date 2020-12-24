# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/chrisecho/__init__.py
# Compiled at: 2016-03-22 09:36:33
import requests

class Echo:

    def doit(self, value):
        return value

    def do_request(self):
        r = requests.get('http://demo.jmbo.org/api/v1/listing/1/?format=json')
        json = r.json
        if callable(json):
            return json()
        else:
            return json