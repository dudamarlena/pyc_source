# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/total_scattering/_version.py
# Compiled at: 2019-10-03 13:34:45
import json
version_json = '\n{\n "date": "2019-10-03T13:24:26-0400",\n "dirty": false,\n "error": null,\n "full-revisionid": "abdf7d9adcb351450045aebdcaaf67a713d60a47",\n "version": "0.2.10"\n}\n'

def get_versions():
    return json.loads(version_json)