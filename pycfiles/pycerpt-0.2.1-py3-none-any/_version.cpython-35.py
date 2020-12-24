# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_version.py
# Compiled at: 2018-03-08 20:19:13
# Size of source mod 2**32: 499 bytes
import json
version_json = '\n{\n "date": "2018-03-08T16:04:08-0800",\n "dirty": false,\n "error": null,\n "full-revisionid": "3e78cc11b390841fed2d8064909dec103f104f3a",\n "version": "0.8.3.1"\n}\n'

def get_versions():
    return json.loads(version_json)