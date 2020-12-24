# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/send_email.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1990 bytes
import json
course = cs_form.get('course', None)
api_token = cs_form.get('api_token', None)
messages = cs_form.get('messages', None)
from_addr = cs_form.get('from_address', None)
error = None
if api_token is None:
    error = 'api_token is required'
elif error is None:
    output = csm_api.get_user_information((globals()), api_token=api_token, course=course)
    if output['ok']:
        uinfo = output['user_info']
        if 'email' not in uinfo['permissions']:
            error = 'Permission Denied'
    elif error is None:
        try:
            messages = json.loads(messages)
        except:
            error = 'error loading messages'

    required_fields = ('recipient', 'subject', 'body')
    if error is None:
        out = []
        for m in messages:
            if any((i not in m for i in required_fields)):
                out.append('Required field missing')
            else:
                out.append(csm_mail.internal_message(globals(), course, m['recipient'], m['subject'], m['body'], from_addr))

    else:
        cs_handler = 'raw_response'
        content_type = 'application/json'
        if error is not None:
            out = {'ok':False, 
             'error':error}
else:
    out = {'ok':True, 
     'responses':out}
response = json.dumps(out)