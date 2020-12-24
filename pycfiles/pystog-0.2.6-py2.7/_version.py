# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pystog/_version.py
# Compiled at: 2018-12-13 08:22:19
import json
version_json = '\n{\n "date": "2018-12-13T08:19:14-0500",\n "dirty": false,\n "error": null,\n "full-revisionid": "106abcdf01e90b5c2e7c656c7c17b8d3221ec44b",\n "version": "0.2.6"\n}\n'

def get_versions():
    return json.loads(version_json)