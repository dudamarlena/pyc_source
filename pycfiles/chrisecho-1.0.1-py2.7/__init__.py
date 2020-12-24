# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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