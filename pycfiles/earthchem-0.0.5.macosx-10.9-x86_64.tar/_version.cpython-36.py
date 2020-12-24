# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/_version.py
# Compiled at: 2018-06-24 21:51:44
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2018-06-25T09:43:54+0800",\n "dirty": false,\n "error": null,\n "full-revisionid": "9cf3973d958680cf28426b4ad5d7962fa69971fb",\n "version": "0.0.5"\n}\n'

def get_versions():
    return json.loads(version_json)