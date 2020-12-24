# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/lib/google_web_server_auth.py
# Compiled at: 2016-04-19 10:47:47
import json

def set_web_server_client_id(app):
    if not app.config['EVENTUM_GOOGLE_AUTH_ENABLED']:
        return
    else:
        _secrets_path = app.config['EVENTUM_CLIENT_SECRETS_PATH']
        try:
            with open(_secrets_path, 'r') as (f):
                _secrets_data = json.loads(f.read())['web']
                app.config['EVENTUM_GOOGLE_CLIENT_ID'] = _secrets_data['client_id']
                if not _secrets_data.get('client_secret', None):
                    raise Exception(('Google Auth config file, {}, missing client secret').format(_secrets_path))
        except IOError:
            raise Exception(('The Google client_secrets file was not found at {}, check that it exists.').format(_secrets_path))

        return