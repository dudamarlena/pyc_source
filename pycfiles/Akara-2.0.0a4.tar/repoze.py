# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/security/repoze.py
# Compiled at: 2013-05-12 18:04:18
from akamu.wheezy import WheezyCachingAdapterSetup
from akara import global_config, request, module_config, response

class requires_authority(object):
    """

    Used with WheezyRepozeWrapper and RepozeWrapper as innermost decorator of
    akara service to indicate that authentication is required and cause
    401 response if there is none.  The first argument is the
    message to send to the client

    @requires_authority('Not authorized')
    def akara_service(): pass

    """

    def __init__(self, message='Not authorized', noauth=False):
        self.message = message
        self.noauth = noauth

    def __call__(self, func):

        def innerHandler(*args, **kwds):
            if 'REMOTE_USER' not in request.environ and not self.noauth:
                response.code = 401
                return self.message
            else:
                if '_' in kwds:
                    del kwds['_']
                return func(*args, **kwds)

        return innerHandler