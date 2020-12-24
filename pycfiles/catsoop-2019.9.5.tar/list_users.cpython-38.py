# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/list_users.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1589 bytes
import json
cs_handler = 'raw_response'
content_type = 'application/json'
course = cs_form.get('course', None)
api_token = cs_form.get('api_token', None)
error = None
if api_token is None or course is None:
    error = 'api_token and course are required'
if error is None:
    output = csm_api.get_user_information((globals()), api_token=api_token, course=course)
    if output['ok']:
        uinfo = output['user_info']
        if 'admin' not in uinfo['permissions']:
            error = 'Permission Denied'
elif error is None:
    output = {'ok':True, 
     'result':csm_user.list_all_users(globals(), course)}
else:
    output = {'ok':False, 
     'error':error}
response = json.dumps(output)