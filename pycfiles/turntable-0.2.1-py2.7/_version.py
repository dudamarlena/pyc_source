# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/turntable/_version.py
# Compiled at: 2015-06-11 21:15:57
import json, sys
version_json = '\n{\n "dirty": false,\n "error": null,\n "full-revisionid": "5c9670f3bb03325afb68290cef4d62cf39888038",\n "version": "0.2.1"\n}\n'

def get_versions():
    return json.loads(version_json)