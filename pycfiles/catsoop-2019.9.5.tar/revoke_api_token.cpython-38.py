# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/revoke_api_token.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1528 bytes
import json
api_token = cs_form.get('api_token', None)
error = None
if api_token is None:
    error = 'api_token is required'
else:
    if error is None:
        output = csm_api.get_user_information((globals()), api_token=api_token)
        if output['ok']:
            uinfo = output['user_info']
        else:
            error = 'Could not get user information'
    if error is not None:
        output = {'ok':False, 
         'error':error}
    else:
        tok = cslog.most_recent('_api_users', [], uinfo['username'], None)
        if tok is not None:
            cslog.overwrite_log('_api_tokens', [], tok, None)
    newtok = csm_api.initialize_api_token(globals(), uinfo)
    output = {'ok':True,  'new_token':newtok}
cs_handler = 'raw_response'
content_type = 'application/json'
response = json.dumps(output)