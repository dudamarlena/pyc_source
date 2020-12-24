# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__UTIL__/api/groups/partner.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 2395 bytes
import json
api_token = cs_form.get('api_token', None)
path = cs_form.get('path', None)
name1 = cs_form.get('username1', None)
name2 = cs_form.get('username2', None)
error = None
if api_token is None:
    error = 'api_token is required'
elif name1 is None:
    error = 'username1 is required'
elif name2 is None:
    error = 'username2 is required'
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
        gnames = ctx.get('cs_group_names', list(map(str, range(100))))
        groups = csm_groups.list_groups(ctx, path)
        secnum = csm_groups.get_section(ctx, path[0], name1)
        sec2 = csm_groups.get_section(ctx, path[0], name2)
        if secnum != sec2:
            error = 'Users are in different sections! (%s and %s)' % (secnum, sec2)
        else:
            taken = groups.get(secnum, {})
        if len(gnames) > 0 and gnames[0] in taken:
            gnames.pop(0)
    else:
        error = csm_groups.add_to_group(ctx, path, name1, gnames[0])
        if error is None:
            error = csm_groups.add_to_group(ctx, path, name2, gnames[0])
        elif error is not None:
            output = {'ok':False, 
             'error':error}
        else:
            output = {'ok': True}
        cs_handler = 'raw_response'
        content_type = 'application/json'
        response = json.dumps(output)