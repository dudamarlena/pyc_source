# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/_version.py
# Compiled at: 2020-02-27 14:06:59
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2020-02-25T14:08:25-0800",\n "dirty": false,\n "error": null,\n "full-revisionid": "dc6eb302815af580cce465185915e8c1257514d0",\n "version": "2.0.3"\n}\n'

def get_versions():
    return json.loads(version_json)