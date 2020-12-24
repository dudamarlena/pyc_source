# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/accounts/middleware.py
# Compiled at: 2016-09-20 14:09:11
# Size of source mod 2**32: 418 bytes
import json

class AuthInfoMiddleware(object):

    def process_template_response(self, request, response):
        if request.user.is_authenticated():
            user = request.user.username
        else:
            user = None
        is_admin = request.user.is_superuser
        response['x-authinfo'] = ';'.join([
         json.dumps(user),
         json.dumps(is_admin)])
        return response