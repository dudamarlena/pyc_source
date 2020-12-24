# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__AUTH__/cert/cert.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1574 bytes


def get_logged_in_user(context):
    env = context['cs_env']
    if 'SSL_CLIENT_S_DN_Email' in env:
        email = env['SSL_CLIENT_S_DN_Email']
        return {'username':email.split('@')[0], 
         'email':email, 
         'name':env['SSL_CLIENT_S_DN_CN']}
    if 'SSL_CLIENT_S_DN' in env:
        cert_data = {}
        for i in env['SSL_CLIENT_S_DN'].split('/'):
            try:
                k, v = i.split('=')
                cert_data[k] = v
            except:
                pass

        email = cert_data.get('emailAddress', 'None')
        return {'username':email.split('@')[0], 
         'email':email, 
         'name':cert_data.get('CN', email)}
    return {'username': 'None'}