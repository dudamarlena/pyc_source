# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/_version.py
# Compiled at: 2016-03-04 05:30:29
# Size of source mod 2**32: 471 bytes
import json, sys
version_json = '\n{\n "dirty": false,\n "error": null,\n "full-revisionid": "5b0dd86cfb471a36e01c6476793b7a1ec82bf833",\n "version": "0.0.5"\n}\n'

def get_versions():
    return json.loads(version_json)