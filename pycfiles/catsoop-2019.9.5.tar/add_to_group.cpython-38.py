# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/groups/add_to_group.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1829 bytes
import json
api_token = cs_form.get('api_token', None)
path = cs_form.get('path', None)
username = cs_form.get('username', None)
group = cs_form.get('group', None)
error = None
if api_token is None:
    error = 'api_token is required'
else:
    if username is None:
        error = 'username is required'
    else:
        if group is None:
            error = 'group is required'
        else:
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
                if error is None:
                    ctx = csm_loader.generate_context(opath)
                    error = csm_groups.add_to_group(ctx, path, username, group)
                if error is not None:
                    output = {'ok':False, 
                     'error':error}
                else:
                    output = {'ok': True}
        cs_handler = 'raw_response'
        content_type = 'application/json'
        response = json.dumps(output)