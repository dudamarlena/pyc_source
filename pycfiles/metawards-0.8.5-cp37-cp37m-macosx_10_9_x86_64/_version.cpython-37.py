# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/_version.py
# Compiled at: 2020-04-22 15:07:58
# Size of source mod 2**32: 586 bytes
import json
version_json = '\n{\n "branch": "devel",\n "date": "2020-04-22T20:07:17+0100",\n "dirty": false,\n "error": null,\n "full-revisionid": "d06137d1839cbfa877d501e85998e54730c17af1",\n "repository": "https://github.com/metawards/MetaWards",\n "version": "0.8.3+12.gd06137d"\n}\n'

def get_versions():
    return json.loads(version_json)