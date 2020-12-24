# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neo/middleware.py
# Compiled at: 2013-05-03 05:25:56


class NeoMiddleware(object):
    """
    This middleware needs to go after AuthenticationMiddleware and SessionMiddleware. It adds the
    user password to the user object on the request. It also processes an exception if the password
    is not in the session, requiring the user to re-authenticate.
    """

    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            pw = request.session.get('raw_password', None)
            if pw:
                request.user.raw_password = pw
        return

    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated():
            if hasattr(request.user, 'old_password') or hasattr(request.user, 'forgot_password_token'):
                request.session['raw_password'] = request.user.raw_password
        return response