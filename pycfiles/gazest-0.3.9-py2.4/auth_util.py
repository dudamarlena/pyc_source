# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/auth_util.py
# Compiled at: 2007-10-17 12:11:28
from webhelpers import *
from authkit.permissions import NotAuthenticatedError, NotAuthorizedError
from authkit.permissions import RemoteUser, RequestPermission
from gazest.lib import helpers as h
from pylons.controllers.util import abort

class HasRank(RequestPermission):
    __module__ = __name__

    def __init__(self, rank):
        self.lvl = h.rank_lvl(rank)

    def check(self, app, environ, start_response):
        user = h.get_remote_user()
        if not user:
            raise NotAuthenticatedError('Not Authenticated')
        if user.rank >= self.lvl:
            return app(environ, start_response)
        else:
            msg = 'You need to be %s or higher to see this page' % h.lvl_rank(self.lvl)
            abort(403, msg)