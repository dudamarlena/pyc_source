# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/minecraft/user.py
# Compiled at: 2018-08-27 03:41:04
# Size of source mod 2**32: 295 bytes
import requests

class ApiBroken(Exception):
    pass


def get_uuid_from_username(username):
    rq = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if rq.status_code == 200:
        json = rq.json()
        return json['id']
    raise ApiBroken