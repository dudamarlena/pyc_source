# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/checkoff/checkoff.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 2453 bytes
defaults = {'csq_npoints': 1}
allow_viewanswer = False
allow_self_submit = False
allow_save = False

def total_points(**info):
    return info['csq_npoints']


def handle_submission(submissions, **info):
    tok, un = submissions[info['csq_name']].split(',')
    i = csm_api.userinfo_from_token(info, tok)
    new = dict(info)
    uinfo = info['csm_auth']._get_user_information(new, new, info['cs_course'], (i or {}).get('username', 'None'), True)
    if 'impersonate' not in uinfo.get('permissions', []):
        percent = 0
        msg = 'You must receive this checkoff from a staff member.'
        l = False
    else:
        new = dict(info)
        new['cs_form'] = {}
        uinfo = info['csm_auth']._get_user_information(new, new, info['cs_course'], un, True)
        if 'checkoff' not in uinfo.get('permissions', []):
            percent = 0
            msg = '%s is not allowed to give checkoffs.' % un
            l = False
        else:
            percent = 1
            now = info['csm_time'].from_detailed_timestamp(info['cs_timestamp'])
            now = info['csm_time'].long_timestamp(now).replace('; ', ' at ')
            msg = 'You received this checkoff from %s on %s.' % (un, now)
            l = True
    return {'score':percent, 
     'msg':msg,  'lock':l}


def render_html(last_log, **info):
    if info['csq_description'] == info['csq_display_name'] == '':
        return ''
    info['csq_description'] = info['csm_language'].source_transform_string(info, info['csq_description'])
    return '<b>%s</b>:<br/>%s' % (info['csq_display_name'], info['csq_description'])


def answer_display(**info):
    return ''