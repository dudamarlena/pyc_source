# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/_version.py
# Compiled at: 2020-05-04 17:05:41
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2020-05-04T22:04:09+0100",\n "dirty": false,\n "error": null,\n "full-revisionid": "5dafe20b7769105b9065a65a281dfe09261bc094",\n "version": "0.4.4"\n}\n'

def get_versions():
    return json.loads(version_json)