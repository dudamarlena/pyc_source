# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyutrack/_version.py
# Compiled at: 2017-10-29 00:01:04
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2017-10-29T12:00:11+0800",\n "dirty": false,\n "error": null,\n "full-revisionid": "149b9c061d0beb768d2735b682af8164d88dfed3",\n "version": "0.7.1"\n}\n'

def get_versions():
    return json.loads(version_json)