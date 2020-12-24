# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/_version.py
# Compiled at: 2020-03-13 12:50:00
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2020-03-11T16:02:33-0400",\n "dirty": false,\n "error": null,\n "full-revisionid": "f6b6961ff101570b7dd2e40012bcad46aa382aa9",\n "version": "0.0.3"\n}\n'

def get_versions():
    return json.loads(version_json)