# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/SteamAuthPy/main.py
# Compiled at: 2017-08-14 10:53:48
from authentication.oauth import finder
from authentication.setup import AddAuthenticator
from authentication.deviceId import getDeviceId
from authentication.guard import SteamGuard
from authentication.login import Login
import json

def guide(self):
    print '\n        All Functions:\n            \n            Show guide - guide();\n                       \n            Get access token - oauth(*path);\n          \n            Generate device id - deviceid(steamid);\n           \n            Add authenticator - setup(steamid, access_token, device id);\n\n            List logged secret keys - secrets();\n\n            Generate two-factor authentication code - authCode(time, secret_key);\n\n            Generate trade offer confirmation key - confkey(time, secret_key, tag_name);\n\n            Send login request - login(username, password, secret_key);\n\n            \n        '


def oauth(*p):
    if len(p) < 1:
        finder(path='authentication/steamchat.html')
    else:
        finder(path=str(p))


def deviceid(steamid):
    if len(str(steamid)) == 17 and str(steamid).isdigit():
        return getDeviceId(str(steamid))
    raise ValueError('Please enter proper steamId')


def setup(steamId, Oauth, UDID, logging=True):
    if len(str(steamId)) == 17 and str(steamId).isdigit():
        addAuth = AddAuthenticator()
        return addAuth.registerAuthenticator(steamId, Oauth, UDID)
    raise ValueError('Please enter proper steamId')


def secrets():
    with open('authentication/shared_secrets.json', 'r') as (data):
        return json.load(data)


def authcode(tm, secret):
    obj = SteamGuard()
    return obj.get_auth_code(int(tm), str(secret))


def confkey(tm, secret, tag):
    obj = SteamGuard()
    return obj.get_confirmation_key(int(tm), str(secret), tag)


def login(username, password, shared_secret):
    _login = Login(str(username), str(password), str(shared_secret))
    return _login.getInfo()