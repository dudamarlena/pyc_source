# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_version.py
# Compiled at: 2020-05-11 13:27:41
# Size of source mod 2**32: 577 bytes
import json
version_json = '\n{\n "branch": "0.11.2)",\n "date": "2020-05-11T18:20:38+0100",\n "dirty": false,\n "error": null,\n "full-revisionid": "bd27ad84819a63ffbe29d81735a653ffd9576062",\n "repository": "https://github.com/metawards/MetaWards",\n "version": "0.11.2"\n}\n'

def get_versions():
    return json.loads(version_json)