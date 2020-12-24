# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/_version.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 463 bytes
import json
version_json = '\n{\n "date": null,\n "dirty": null,\n "error": "unable to compute version",\n "full-revisionid": null,\n "version": "0+unknown"\n}\n'

def get_versions():
    return json.loads(version_json)