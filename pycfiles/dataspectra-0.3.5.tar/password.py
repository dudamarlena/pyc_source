# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/scripts/password.py
# Compiled at: 2018-02-08 18:28:30
import base64

def basicAuth(func):

    def callf(webappRequest, *args, **kwargs):
        auth_header = webappRequest.request.headers.get('Authorization')
        if auth_header == None:
            webappRequest.response.set_status(401, message='Authorization Required')
            webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="Unsecure Area"'
        else:
            auth_parts = auth_header.split(' ')
            user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
            user_arg = user_pass_parts[0]
            pass_arg = user_pass_parts[1]
            if user_arg != 'guest' or pass_arg != 'barres':
                webappRequest.response.set_status(401, message='Authorization Required')
                webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
            else:
                return func(webappRequest, *args, **kwargs)
        return

    return callf