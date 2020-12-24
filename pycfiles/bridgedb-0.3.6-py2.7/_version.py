# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/_version.py
# Compiled at: 2016-07-29 18:59:30
import json, sys
version_json = '\n{\n "dirty": false,\n "error": null,\n "full-revisionid": "936958ae0bb138bf1a85cd311488da0c01fe2a57",\n "version": "0.3.6"\n}\n'

def get_versions():
    return json.loads(version_json)