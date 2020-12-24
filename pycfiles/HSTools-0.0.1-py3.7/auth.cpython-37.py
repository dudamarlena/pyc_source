# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/auth.py
# Compiled at: 2019-10-18 09:44:23
# Size of source mod 2**32: 1982 bytes
import os, json, base64, pickle, hs_restclient

def basic_authorization(authfile='~/.hs_auth_basic'):
    """
    performs basic HS authorization using username and password stored in
    ~/.hs_auth_basic file in the following format (b64 encoded):

    {
        "usr": "<username>"
        "pwd": "<password>"
    }

    Returns hs_restclient instance or None
    """
    authfile = os.path.expanduser(authfile)
    if not os.path.exists(authfile):
        raise Exception(f"Could not find authentication file [.hs_auth] at {authfile}")
    try:
        with open(authfile, 'r') as (f):
            txt = f.read()
            d = base64.b64decode(txt)
            creds = json.loads(d.decode())
            a = hs_restclient.HydroShareAuthBasic(username=(creds['usr']), password=(creds['pwd']))
            hs = hs_restclient.HydroShare(auth=a)
            hs.getUserInfo()
            return hs
    except Exception as e:
        try:
            raise Exception(e)
        finally:
            e = None
            del e


def oauth2_authorization(authfile='~/.hs_auth'):
    """
    performs HS authorization using OAuth2 credentials stored in
    ~/.hs_auth file, in a pickled binary format.

    Returns hs_restclient instance or None
    """
    authfile = os.path.expanduser(authfile)
    if not os.path.exists(authfile):
        raise Exception(f"Could not find authentication file [.hs_auth] at {authfile}")
    try:
        with open(authfile, 'rb') as (f):
            token, cid = pickle.load(f)
            a = hs_restclient.HydroShareAuthOAuth2(cid, '', token=token)
            hs = hs_restclient.HydroShare(auth=a)
            hs.getUserInfo()
            return hs
    except Exception as e:
        try:
            raise Exception(e)
        finally:
            e = None
            del e