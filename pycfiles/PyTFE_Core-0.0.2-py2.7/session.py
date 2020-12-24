# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tfe/core/session.py
# Compiled at: 2018-10-14 15:04:40
import requests, sys
from tfe.core.exception import RaisesTFEException

class TFESession(object):
    base_url = 'https://app.terraform.io'
    atlas_token = None
    session_headers = None
    session = None

    def __init__(self, api, token):
        TFESession.atlas_token = token
        TFESession.base_url = api
        TFESession.session = requests.Session()
        TFESession.session.headers = {'Authorization': ('Bearer {0}').format(token), 
           'Content-Type': 'application/vnd.api+json'}
        TFESession.session_headers = TFESession.session.headers