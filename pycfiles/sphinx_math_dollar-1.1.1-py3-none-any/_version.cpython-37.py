# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aaronmeurer/Documents/sphinx-math-dollar/build/lib/sphinx_math_dollar/_version.py
# Compiled at: 2019-09-17 19:56:58
# Size of source mod 2**32: 495 bytes
import json
version_json = '\n{\n "date": "2019-09-17T18:10:38-0500",\n "dirty": false,\n "error": null,\n "full-revisionid": "9ab14f3c2c5c40c65d658bec6c24ddddf74314e8",\n "version": "1.1"\n}\n'

def get_versions():
    return json.loads(version_json)