# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/groups/get_my_group.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1944 bytes
import json
api_token = cs_form.get('api_token', None)
path = cs_form.get('path', None)
_as = cs_form.get('as', None)
error = None
if api_token is None:
    error = 'api_token is required'
try:
    path = opath = json.loads(path)
except:
    error = 'invalid path: %s' % path
else:
    if error is None:
        output = csm_api.get_user_information((globals()),
          api_token=api_token, course=(path[0]), _as=_as)
        if output['ok']:
            uinfo = output['user_info']
        else:
            error = 'Could not get user information'
    else:
        if error is None:
            ctx = csm_loader.generate_context(opath)
            section, group, members = csm_groups.get_group(ctx, path, uinfo['username'])
            if section is None:
                if group is None:
                    error = '%s has not been assigned to a group' % uinfo['username']
                    members = [uinfo['username']]
            members = list(sorted(members, key=(lambda x: (0 if x == uinfo['username'] else 1, x))))
        if error is not None:
            output = {'ok':False, 
             'error':error}
        else:
            output = {'ok':True, 
             'section':section,  'group':group,  'members':members}
    cs_handler = 'raw_response'
    content_type = 'application/json'
    response = json.dumps(output)