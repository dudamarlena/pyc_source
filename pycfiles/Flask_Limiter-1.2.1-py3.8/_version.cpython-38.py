# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/flask_limiter/_version.py
# Compiled at: 2020-02-26 13:57:27
# Size of source mod 2**32: 497 bytes
import json
version_json = '\n{\n "date": "2020-02-26T10:57:24-0800",\n "dirty": false,\n "error": null,\n "full-revisionid": "db6599307ba1cf8ffc7667619e5fa3ecff8c21d5",\n "version": "1.2.1"\n}\n'

def get_versions():
    return json.loads(version_json)