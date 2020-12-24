# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_version.py
# Compiled at: 2018-05-29 16:27:17
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2018-05-29T13:26:34-0700",\n "dirty": false,\n "error": null,\n "full-revisionid": "f0b7172235f5201ed71b0424a6eb377e9ac9907d",\n "version": "0.1.0"\n}\n'

def get_versions():
    return json.loads(version_json)