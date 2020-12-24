# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/groups/overwrite_groups.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1884 bytes
import json
api_token = cs_form.get('api_token', None)
path = cs_form.get('path', None)
section = cs_form.get('section', None)
groups = cs_form.get('groups', None)
error = None
if api_token is None:
    error = 'api_token is required'
elif groups is None:
    error = 'groups (JSON) is required'
try:
    path = opath = json.loads(path)
except:
    error = 'invalid path: %s' % path
else:
    if error is None:
        output = csm_api.get_user_information((globals()),
          api_token=api_token, course=(path[0]))
        if output['ok']:
            uinfo = output['user_info']
            if 'groups' not in uinfo['permissions']:
                if 'admin' not in uinfo['permissions']:
                    error = 'Permission Denied'
try:
    groups = json.loads(groups)
except:
    error = 'error loading groups JSON' + str(groups)
else:
    if error is None:
        ctx = csm_loader.generate_context(opath)
        error = csm_groups.overwrite_groups(ctx, path, section, groups)
    elif error is not None:
        output = {'ok':False, 
         'error':error}
    else:
        output = {'ok': True}
    cs_handler = 'raw_response'
    content_type = 'application/json'
    response = json.dumps(output)