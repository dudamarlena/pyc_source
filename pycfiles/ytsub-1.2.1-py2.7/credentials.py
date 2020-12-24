# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ytsub/credentials.py
# Compiled at: 2013-01-11 15:47:57
import pkgutil, tempfile, oauth2client.clientsecrets as clientsecrets, oauth2client, sys
from os.path import expanduser
from os import pathsep
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

def acquire_credentials(scopes):
    client_secrets_contents = pkgutil.get_data('ytsub', 'data/client_secrets.json')
    if client_secrets_contents is None:
        sys.exit('Missing clientsecrets.json file.')
    try:
        client_type, client_info = clientsecrets.loads(client_secrets_contents)
        if client_type in [clientsecrets.TYPE_WEB, clientsecrets.TYPE_INSTALLED]:
            flow = OAuth2WebServerFlow(client_info['client_id'], client_info['client_secret'], scopes, redirect_uri=client_info['redirect_uris'], user_agent=None, auth_uri=client_info['auth_uri'], token_uri=client_info['token_uri'])
    except clientsecrets.InvalidClientSecretsError:
        sys.exit('Invalid client secrets file.')

    storage = Storage(expanduser('~') + '/.ytsub-oauth2.json')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)
    return credentials