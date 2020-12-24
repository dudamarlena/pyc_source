# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__AUTH__/dummy/dummy.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1084 bytes


def get_logged_in_user(context):
    if context.get('cs_form', {}).get('loginaction', None) == 'logout':
        return {}
    uname = context['cs_dummy_username']
    return {'username':uname, 
     'name':context.get('cs_dummy_name', uname), 
     'email':context.get('cs_dummy_email', uname)}