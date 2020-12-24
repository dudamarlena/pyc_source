# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/_version.py
# Compiled at: 2020-04-17 17:56:18
# Size of source mod 2**32: 575 bytes
import json
version_json = '\n{\n "branch": "master",\n "date": "2020-04-17T22:55:01+0100",\n "dirty": false,\n "error": null,\n "full-revisionid": "03eb79a365977c1578293fa7eebd476afc78e835",\n "repository": "https://github.com/metawards/MetaWards",\n "version": "0.7.1"\n}\n'

def get_versions():
    return json.loads(version_json)