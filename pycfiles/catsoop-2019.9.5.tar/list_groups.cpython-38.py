# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/groups/list_groups.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 2567 bytes
import json
api_token = cs_form.get('api_token', None)
path = cs_form.get('path', None)
section = cs_form.get('section', None)
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
          api_token=api_token, course=(path[0]))
        if output['ok']:
            uinfo = output['user_info']
            if 'groups' not in uinfo['permissions']:
                if 'admin' not in uinfo['permissions']:
                    error = 'Permission Denied'
    elif error is not None:
        output = {'ok':False, 
         'error':error}
    else:
        ctx = csm_loader.generate_context(opath)
        groups = csm_groups.list_groups(ctx, path)
        all_students = {csm_user.read_user_file(globals(), path[0], i, {}):i for i in csm_user.list_all_users(globals(), path[0])}
        if section is not None:
            groups = groups.get(section, {})
            all_partnered = sum(groups.values(), [])
            unpartnered = [i for i in all_students if i not in all_partnered if str(all_students[i].get('section', 'default')) == section]
            groups['_unpartnered'] = unpartnered
        else:
            for section in groups:
                secgrp = groups[section]
                all_partnered = sum(secgrp.values(), [])
                unpartnered = [i for i in all_students if i not in all_partnered if str(all_students[i].get('section', 'default')) == section]
                secgrp['_unpartnered'] = unpartnered

        output = {'ok':True, 
         'groups':groups}
    cs_handler = 'raw_response'
    content_type = 'application/json'
    response = json.dumps(output)