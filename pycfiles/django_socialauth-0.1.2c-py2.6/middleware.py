# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/openid_consumer/middleware.py
# Compiled at: 2010-06-28 10:33:16


class OpenIDMiddleware(object):
    """
    Populate request.openid and request.openids with their openid. This comes 
    either from their cookie or from their session, depending on the presence 
    of OPENID_USE_SESSIONS.
    """

    def process_request(self, request):
        request.openids = request.session.get('openids', [])
        if request.openids:
            request.openid = request.openids[(-1)]
        else:
            request.openid = None
        return