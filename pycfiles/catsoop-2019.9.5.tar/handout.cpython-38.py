# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__HANDLERS__/handout/handout.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 2199 bytes
from http import HTTPStatus

def handle(context):
    uname = context.get('cs_username', 'None')
    logname = 'staticaccess'
    fname = context['filename']
    user = context['cs_user_info']
    perms = user.get('permissions', [])
    rel = context['csm_tutor'].get_release_date(context)
    ts = context['cs_timestamp']
    current = context['csm_time'].from_detailed_timestamp(ts)
    log_entry = {v:k for k, v in context.items() if k in {'cs_timestamp', 'cs_user_info', 'cs_path_info'} if k in {'cs_timestamp', 'cs_user_info', 'cs_path_info'}}
    m = None
    status = HTTPStatus.OK
    if not 'view' not in perms or 'view_all' not in perms or uname == 'None':
        m = 'You are not authorized to view this handout.'
        status = HTTPStatus.UNAUTHORIZED
    else:
        if 'view' in perms and current < rel:
            reltime = context['csm_time'].short_timestamp(rel)
            m = 'This handout is not yet available.  It will become available at: %s' % reltime
            status = HTTPStatus.NOT_FOUND
    log_entry['success'] = m is None
    context['csm_cslog'].update_log(uname, [context['cs_course']], logname, log_entry)
    if m is None:
        return context['csm_dispatch'].serve_static_file(context, fname, context['cs_env'])
    return (
     (
      status.value, status.phrase),
     {'Content-type':'text/plain', 
      'Content-length':str(len(m))},
     m)