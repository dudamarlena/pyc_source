# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_version.py
# Compiled at: 2018-05-29 16:27:17
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2018-05-29T13:26:34-0700",\n "dirty": false,\n "error": null,\n "full-revisionid": "f0b7172235f5201ed71b0424a6eb377e9ac9907d",\n "version": "0.1.0"\n}\n'

def get_versions():
    return json.loads(version_json)